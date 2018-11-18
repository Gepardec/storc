#!/bin/sh

PRG=$0
MY_PATH=$(readlink -f $PRG)
BIN_DIR=`dirname $MY_PATH`
BASE_DIR=`dirname $BIN_DIR`
LIB_DIR=$BASE_DIR/lib
CONFIG_DIR=$BASE_DIR/conf

CP=$CONFIG_DIR
for f in $LIB_DIR/*.jar; do
    if [ x"$CP" = x ]; then
      CP=$f
    else
      CP=$CP:$f
    fi
done

java -cp $CP at.gepardec.demobatch.Hello || { echo "Failed executing batch!" 1>&2;  exit 1; }
test -d $BASE_DIR/var || { echo "Verzeichnis var existiert nicht!" 1>&2;  exit 1; }
test -d $BASE_DIR/tmp || { echo "Verzeichnis tmp existiert nicht!" 1>&2;  exit 1; }
test -d $BASE_DIR/ext || { echo "Verzeichnis ext existiert nicht!" 1>&2;  exit 1; }
test -d $BASE_DIR/log || { echo "Verzeichnis log existiert nicht!" 1>&2;  exit 1; }
test -f $BASE_DIR/README.txt || { echo "Datei README.txt existiert nicht!" 1>&2;  exit 1; }
echo "Finnished OK"
