FROM centos:7

RUN yum install -y epel-release && \
    yum install -y ansible git python python-pip java-1.8.0-openjdk unzip && \
    ln -s /usr/lib/jvm/java-1.8.0-openjdk-1.8.*/jre /usr/lib/jvm/jdk1.8.0_144
# symlink is only a quick fix and may break in the future
# ansible playbook should check if lxml is installed before using maven_artefact

COPY jboss-eap-7.1.0.zip /root/.m2/repository/org/jboss/jboss-eap/7.1.0/jboss-eap-7.1.0.zip
COPY . /opt/storc
COPY testruns/projects/servlet-with-logging/target/. /root/.m2/repository/at/test/servlet-with-logging/1.1.0/.
WORKDIR /opt/storc/testruns

CMD  ansible-playbook pb_install_sevlet_with_logging.yml -e host=demo_dev -v