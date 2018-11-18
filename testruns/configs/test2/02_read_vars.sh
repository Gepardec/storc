
f=../../tmp1
:> $f
echo Hello >> $f
echo $PATH  >> $f
echo "Working dir: " `pwd` >> $f 2>&1
java -version >> $f 2>&1
echo TEST: $TEST >> $f 2>&1
echo TEST1: $TEST1 >> $f 2>&1
echo TEST3: $TEST3 >> $f 2>&1
echo JBOSS_HOME: $JBOSS_HOME  >> $f
echo JBOSS_PORT_OFFSET: $JBOSS_PORT_OFFSET >> $f 2>&1
