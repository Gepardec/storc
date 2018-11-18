#!/usr/bin/python

DOCUMENTATION = '''
---
module: wildfly_configure
short_description: Configure JBoss WildFly.
description: Configure JBoss WildFly or EAP with help of jboss-cli.sh
'''

EXAMPLES = '''
- name: Show deployments
  wildfly_configure:
    command: ls /deployments
'''

RETURN = '''
result:
    description: Output of command
    returned: success
    type: string
    sample: xxx
'''

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os
import time
import zipfile
import re
import logging

__author__ = 'Erhard Siegl'

# Global variables
standalone_sh = ""
pidfile = ""
jboss_home = ""
jboss_cli = ""
jboss_port_offset = 0
jboss_version = ""
jboss_rc_file = ""
log_out = []

def configure(data):

    is_error = False
    has_changed = False

    initialise(data)

    result = "UNDEFINED"
    if data['command']:
        is_error, result = do_comand( data['command'])

    if data['clifile']:
        is_error, result = do_cli_file( data['clifile'])

    if data['file']:
        is_error, result = do_file( data['file'])

    if data['dir']:
        is_error, result = do_dir( data['dir'])

    if data['start']:
        is_error, result = do_start()

    if data['stop']:
        is_error, result = do_stop()

    if data['restart']:
        is_error, result = do_restart()

    if data['status']:
        is_error, result = do_status()

    if "UNDEFINED" == result:
        result = "No command given"
        is_error = True
        has_changed = False

    resp = {
        "result": result
    }
    if is_error:
        meta = {"status" : "FAILED", "response" : resp, "out" : log_out}
    else:
        meta = {"status" : "OK", "response" : resp, "out" : log_out}

    return is_error, has_changed, meta

def initialise( data):
    global pidfile
    global standalone_sh
    global jboss_cli
    global jboss_port_offset
    global jboss_home
    global jboss_version
    global jboss_rc_file
    global log_out

    jboss_version = data['jboss_version']
    jboss_home = data['jboss_home']
    jboss_rc_file = data['jboss_rc_file']
    jboss_port_offset =  data['jboss_port_offset']

    read_jboss_rc_file()
    jboss_version = discover_version(jboss_home, jboss_version)

    jboss_cli = jboss_home + '/bin/jboss-cli.sh'
    standalone_sh = jboss_home + '/bin/standalone.sh'
    rundir = jboss_home + '/standalone'
    pidfile = rundir + '/pid.lock'

    logdir = jboss_home + '/standalone/log'
    if not os.path.exists(logdir):
      os.makedirs(logdir)
    log_out.append( "Logfile: " + logdir + "/ansible.log")
    logging.basicConfig(filename=logdir + "/ansible.log", level=logging.DEBUG)


def jboss_admin_connection():
    port = base_port(jboss_version) + jboss_port_offset
    return "localhost:" + str(port)
    

def discover_version(jboss_home, jboss_version):

    version_file = jboss_home + '/version.txt'

    if not os.path.exists(version_file):
        return

    for line in open(version_file):
        if "Version" in line:
            p = re.compile('.*?Version (.+)')
            version = p.match(line).group(1)
            jboss_version = "jboss_eap_" + version
    return jboss_version


def base_port(jboss_version):
    p = re.compile('.*?(\d+)')
    version = int(p.match( jboss_version).group(1))
    if "eap" in jboss_version:
      if version == 6:
        major = 7
      else:
        major = 10
    else:
      major = version

    if major == 7:
      return 9999
    else:
      return 9990

def do_comand( command):
    logging.debug(jboss_cli + " --connect" + " --controller=" + jboss_admin_connection() + " " + command)
    return execute(
      subprocess.Popen(["sh", jboss_cli, "--connect", "--controller=" + jboss_admin_connection(), command],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=get_environment())
    )

def do_cli_file( file):
    logging.debug(jboss_cli + " --connect" + " --controller=" + jboss_admin_connection() + " --file=" + file)
    return execute(
      subprocess.Popen(["sh", jboss_cli, "--connect", "--controller=" + jboss_admin_connection(), "--file=" + file], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=get_environment())
    )

def do_sh_file( file):
    logging.debug( "sh " + file)
    return execute(
      subprocess.Popen(["sh", file], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=get_environment())
    )

def do_zip_file( file):
    logging.debug( "unzip " + file)
    return unzip( file, jboss_home)

def do_module_file( file):
    logging.debug( "module unzip " + file)
    return unzip( file, jboss_home + "/modules")

def do_bootstrap():
    bootstrap = "00_BOOTSTRAP"
    if not os.path.isfile(bootstrap):
      logging.info("Bootstrap file " + bootstrap + " does not exist.")
      return False, "No " + bootstrap
    logging.info("Handle Bootstrap file " + bootstrap)
    return do_sh_file( bootstrap);

def do_file( file):
    global log_out
    logging.debug( "do_file " + file)
    log_out.append( "File:" + file)
    filename, ext = os.path.splitext(file)
    dir = os.path.dirname(file)
    basename = os.path.basename(file)
    if dir:
      os.chdir(dir)
    if ext == ".cli":
      return do_cli_file(basename);
    if ext == ".conf":
      return do_cli_file(basename);
    if ext == ".sh":
      return do_sh_file(basename);
    if ext == ".zip":
      return do_zip_file(basename);
    if ext == ".module":
      return do_module_file(basename);
    if ext == ".restart":
      return do_restart();
    logging.info( "Ignore file " + file)
    log_out.append( "Ignore file:" + file)
    return False, "Ignore file " + file

def do_dir( dir):
    global log_out
    log_out.append( "Config-Dir: " + dir)
    logging.debug( "do_dir " + dir)
    error = False
    result = ""

    os.chdir(dir)
    error, result = do_bootstrap()
    if error:
      logging.error( "error " + str(error) + " result: " + result)
      return error, result

    listing = sorted(os.listdir("./"))
    for file in listing:
      error, result = do_file(file)
      if error:
        logging.error( "error " + str(error) + " result: " + result)
        return error, result
    return False, "Done directory " + dir

def do_start():
    if is_running():
      return False, "already started"

    logdir = jboss_home + "/standalone/log"
    if not os.path.exists(logdir):
      os.makedirs(logdir)
    outlog = logdir + "/out.log"
    f = open(outlog, 'w')
    subprocess.Popen(["nohup", standalone_sh, "-Djboss.socket.binding.port-offset=" + str(jboss_port_offset) ],
        stdout=f, stderr=f, env=get_environment())
    return wait_for_started()

def do_stop():
    if not is_running():
      return False, "not running"

    error, result = do_comand( "/:shutdown")
    if error:
      return True, "Shutdown failed: " + result

    return wait_for_stopped()

def do_restart():
    error, result = do_stop()
    if error:
      return error, result
    return do_start()

def do_status():
    info = ""
    info += " standalone.sh: " + standalone_sh
    info += " jboss_admin_connection: " + jboss_admin_connection()
    info += " is running: " + str(is_running())
    info += " jboss_version: " + jboss_version
    info += " JAVA_HOME: " +  os.environ['JAVA_HOME'] 
    return False, info

def is_running():
    pid = get_pid()
    if pid == 0: return False
    return is_process_running( pid)

def wait_for_started():
    TIMEOUT = 30
    starttime = int(time.time())
    while timediff(starttime) < TIMEOUT:
      time.sleep(1)
      if not is_running():
        return True, "Process not started sucessfully after " + str(timediff(starttime)) + "sec"
      if wildfly_is_started():
        return False, "Started after " + str(timediff(starttime)) + "sec"

    return True, "Process seems to run, but start not finnished within timeout of " + str(TIMEOUT) + "sec."

def wait_for_stopped():
    STOP_TIMEOUT = 20
    starttime = int(time.time())
    while timediff(starttime) < STOP_TIMEOUT:
      time.sleep(1)
      if not is_running():
        return False, "Shutdown after " + str(timediff(starttime)) + "sec"

    return True, "Not stopped after " + str(STOP_TIMEOUT) + "sec."

def timediff( starttime):
    return int(time.time()) - starttime

def wildfly_is_started():
    command = "./:read-attribute(name=server-state)"
    error, result = do_comand( command)
    if error:
      return False
    if "running" in result:
      return True
    return False

def is_process_running(process_id):
    try:
      os.kill(process_id, 0)
      return True
    except OSError:
      return False

def get_pid( ):
    if not os.path.isfile( pidfile):
      return 0
    with open(pidfile, 'r') as f:
      pid = f.read()
    return int( pid)

def execute(p):
    global log_out
    result,err = p.communicate()
    if p.returncode != 0:
        return True, result + err

    logging.info( result)
    log_out.append( result)
    return False, result

def unzip( zip, dest):
    zip_ref = zipfile.ZipFile(zip, 'r')
    try: # Workaround for problem in Python 2.6,
         # use ZipFile.extractall in future versions
      for info in zip_ref.infolist():
        if (info.external_attr >> 31) > 0: # is not directory?
          real_path = zip_ref.extract(info, dest)
          if not real_path:
            return True, "Extract failed: " + info.filename
        else:
          dir = os.path.join(dest, info.filename)
          if not os.path.exists(dir):
            os.makedirs(dir)

        # permission
        unix_attributes = info.external_attr >> 16
        target = os.path.join(dest, info.filename)
        if unix_attributes:
            os.chmod(target, unix_attributes)

    finally:
      zip_ref.close()
    return False, "Unzipped " + zip

def read_jboss_rc_file():
    global jboss_home
    global jboss_port_offset
    global jboss_version

    my_env = {}
    if os.path.exists(jboss_rc_file):
        with open(jboss_rc_file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                if not line.strip(): # Ignore empty or only spaces
                    continue
                 # key, value = line.replace('export ', '', 1).strip().split('=', 1)
                key, value = line.strip().split('=', 1)
                my_env[key] = os.path.expandvars(value)

    if "JBOSS_PORT_OFFSET" in my_env:
        jboss_port_offset = int(my_env["JBOSS_PORT_OFFSET"])
    if "JBOSS_HOME" in my_env:
        jboss_home = my_env["JBOSS_HOME"]
    if "JBOSS_RELEASE_NAME" in my_env:
        jboss_version = my_env["JBOSS_RELEASE_NAME"]
    if "JBOSS_PIDFILE" in my_env:
        jboss_version = my_env["JBOSS_PIDFILE"]

def get_environment( ):
    # my_env = os.environ.copy()
    my_env = os.environ
    my_env["JBOSS_PORT_OFFSET"] = str(jboss_port_offset)
    my_env["JBOSS_HOME"] = jboss_home
    my_env["JBOSS_RELEASE_NAME"] = jboss_version
    my_env["JBOSS_PIDFILE"] = pidfile
    my_env["LAUNCH_JBOSS_IN_BACKGROUND"] = "true"

    if os.path.exists(jboss_rc_file):
        with open(jboss_rc_file) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                if not line.strip(): # Ignore empty or only spaces
                    continue
                 # key, value = line.replace('export ', '', 1).strip().split('=', 1)
                key, value = line.strip().split('=', 1)
                my_env[key] = os.path.expandvars(value)
    return my_env

def main():
    fields = {
        "jboss_home": {
            "required": True,
            "type": "str"
        },
        "jboss_port_offset": {
            "required": False,
            "default" : 0,
            "type": "int"
        },
        "jboss_version": {
            "required": False,
            "default" : "jboss-eap-6.0.0",
            "type": "str"
        },
        "jboss_rc_file": {
            "required": False,
            "default" : "",
            "type": "str"
        },
        "command": {
            "required": False,
            "type": "str"
        },
        "file": {
            "required": False,
            "type": "str"
        },
        "clifile": {
            "required": False,
            "type": "str"
        },
        "dir": {
            "required": False,
            "type": "str"
        },
        "start": {
            "required": False,
            "type": "str", 
			"default": "no", 
            "type": "bool"
        },
        "stop": {
            "required": False,
            "type": "str", 
			"default": "no", 
            "type": "bool"
        },
        "restart": {
            "required": False,
            "type": "str", 
			"default": "no", 
            "type": "bool"
        },
        "status": {
            "required": False,
            "type": "str", 
			"default": "no", 
            "type": "bool"
        },
    }

    module = AnsibleModule(argument_spec=fields)

    is_error, has_changed, result = configure(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error configure WildFly", meta=result)

if __name__ == '__main__':
    main()

