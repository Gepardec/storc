#!/bin/sh

PRG=$0
MY_PATH=$(readlink -f $PRG)
SCRIPTS_DIR=`dirname $MY_PATH`
ANSIBLECONFIG_DIR=`dirname $SCRIPTS_DIR`

# Umgebung setzen
#source /home/ansible/hacking/env-setup

#set -x
cd $ANSIBLECONFIG_DIR || exit 1

#Befuellen der uebergebenen Variablen
INSTANZ="not_set"
NEXUS_GROUP_ID="not_set"
NEXUS_ARTIFACT_ID="not_set"
NEXUS_ARTIFACT_VERSION="not_set"
NEXUS_CLASSIFIER=pkg
KUNDE=""
STAGE=""

#####################################################################
##                      print_usage
#####################################################################
print_usage(){
cat <<EOF 1>&2
usage: $PRG [-h] [-i instanz] [-g group_id] [-a artefact_id] [-v version] [-c classifier] [-k kunde] [-s stage] 
       
Optionen:
    i instanz: Name der Instanz auf der das Paket installiert werden soll
    a artefact_id: Maven Artefact-Id des Installationspaketes
    g group_id: Maven Group-Id des Installationspaketes
    v version: Maven Version des Installationspaketes
    c classifier: Maven Classifier des Installationspaketes. Default: $NEXUS_CLASSIFIER
    k kunde: Kundenbezeichner der Instanz (z.B: CUST1, CUST2,...)
    s stage: Stage-Bezeichnung der Instanz (z.B: ET, FT, ST, PR,...)
    h: Diese Hilfeseite

Deployed ein durch Maven-Koordinaten angegebenes Installationspaket auf einer Instanz.

EOF
}

######################   Optionen bestimmen ###################

while getopts "i:a:g:v:c:k:s:h" option
do
    case $option in
      i) INSTANZ=$OPTARG;;
      a) NEXUS_ARTIFACT_ID=$OPTARG;;
      g) NEXUS_GROUP_ID=$OPTARG;;
      c) NEXUS_CLASSIFIER=$OPTARG;;
      v) NEXUS_ARTIFACT_VERSION=$OPTARG;;
      k) KUNDE=$OPTARG;;
      s) STAGE=$OPTARG;;
      *)
        print_usage
        exit 1
        ;;
    esac
done

shift `expr $OPTIND - 1`


echo "Starte Holen der aktuellsten Stages aus dem GIT-Repo"
echo "git pull ../STAGES/$KUNDE/$STAGE" 
( cd ../STAGES/$KUNDE/$STAGE && git pull ) || echo "WARNING: Error pulling from git"

echo "Starte Holen der aktuellsten Sourcen aus dem GIT-Repo in " `pwd`
echo "git pull" 
git pull

ansible-playbook pb/PB_wildfly_install.yml -v -i ../STAGES/$KUNDE/$STAGE/inventory -e host=$INSTANZ -e group_id=$NEXUS_GROUP_ID -e artifact_id=$NEXUS_ARTIFACT_ID -e version=$NEXUS_ARTIFACT_VERSION -e classifier=$NEXUS_CLASSIFIER

