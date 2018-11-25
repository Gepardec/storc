#!/bin/bash

PRG=`readlink -e $0`
DIR=`dirname $PRG`

java -jar $DIR/h2-*.jar -tcpAllowOthers 
