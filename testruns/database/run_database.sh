#!/bin/bash

PRG=`readlink -e $0`
DIR=`dirname $PRG`

java -jar $DIR/h2-1.3.175.jar -tcpAllowOthers 
