Verzeichnis zum Testen der Skripts
==================================

Voraussetzungen für Demo-Beispiele
----------------------------------

Maven installiert
JBoss EAP oder WildFly ZIP-Datei vorhanden
[Flyway Zip-Datei](https://flywaydb.org/documentation/commandline/#download-and-installation) vorhanden

JBoss und Flyway ins lokale Repository installieren
---------------------------------------------------
```
VERSION=7.1.0
mvn install:install-file -Dfile=$HOME/Downloads/jboss-eap-$VERSION.zip -DgroupId=org.jboss \
    -DartifactId=jboss-eap -Dversion=$VERSION -Dpackaging=zip

VERSION=5.2.1
mvn install:install-file -Dfile=$HOME/Downloads/flyway-commandline-$VERSION.zip -DgroupId=org.flywaydb \
    -DartifactId=flyway-commandline -Dversion=$VERSION -Dpackaging=zip
```

Kompilieren der Beispiele
-------------------------

```
 cd projects
 mvn install
```



Beispiel
```
 ansible-playbook pb_install_sevlet_with_logging.yml -e host=demo_dev

 ./database/run_database.sh &
 ansible-playbook pb_test_db_app.yml -e host=demo_dev
```

oder mit Skript

```
 mkdir ../../STAGES/
 ln -s `pwd`/host_vars ../../STAGES/
 ln -s `pwd`/inventory ../../STAGES/

```

```
 ../bin/deploy.sh -i demo_dev  -a servlet-with-logging -g at.test -v 1.1.0

 ./database/run_database.sh &
 ../bin/deploy.sh -i demo_dev  -a servlet-with-db -g at.test -v 1.1.0
```
