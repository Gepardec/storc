Run storc - paramters
=============
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
