#!/bin/sh

PRG=$0
echo "Start $0 " `date`

#####################################################################
##                      print_usage
#####################################################################
print_usage(){
cat <<EOF 1>&2
usage: $PRG [-h] [-a artefact] [-b dir] [-v version]
Optionen:
    a artefact: Artefact-Id der Flyway Maven-Koordinaten
    b dir: Basisverzeichnis in das Flyway ausgepackt wurde
    v version: Version der Flyway Maven-Koordinaten
    h: Diese Hilfeseite

Ausfuehren der Datenbank-Migration mit Flyway. Das Skript wird
normalerweise von einem Ansible-Skript aufgerufen.

EOF
}

#####################################################################
##                      print_settings
#####################################################################
print_settings(){
cat <<EOF

Settings:
----------------------
FLYWAY_ARTEFACT=$FLYWAY_ARTEFACT
FLYWAY_HOME=$FLYWAY_HOME
FLYWAY_VERSION=$FLYWAY_VERSION
FLYWAY_COMMANDFILE=$FLYWAY_COMMANDFILE
FLYWAY_CONFIG=$FLYWAY_CONFIG
FLYWAY_SQL=$FLYWAY_SQL
CONFIG_DIR=$CONFIG_DIR
----------------------
EOF
}

######################   Optionen bestimmen ###################
 
while getopts "a:b:v:h" option  
do 
    case $option in
      a) FLYWAY_ARTEFACT=$OPTARG;;
      b) FLYWAY_HOME=$OPTARG;;
      v) FLYWAY_VERSION=$OPTARG;;
      *) 
        print_usage
        exit 1
        ;;
    esac 
done

shift `expr $OPTIND - 1`


MY_PATH=$(readlink -f $PRG)
CONFIG_DIR=`dirname $MY_PATH`

if [ x$FLYWAY_HOME = x ]; then
        echo "Flyway-Home ist nicht gesetzt!" 1>&2
        exit 1
fi

FLYWAY_COMMANDFILE=$FLYWAY_HOME/flyway-$FLYWAY_VERSION/flyway
FLYWAY_CONFIG=$CONFIG_DIR/flyway.conf
FLYWAY_SQL=$CONFIG_DIR/../sql

print_settings

sh $FLYWAY_COMMANDFILE -configFile=$FLYWAY_CONFIG -locations=filesystem:$FLYWAY_SQL migrate

