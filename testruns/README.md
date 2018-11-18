Verzeichnis zum Testen der Skripts
==================================

Beispiel
```
 ansible-playbook pb_test_scripts.yml -e host=test_esiegl -v
 ansible-playbook pb_install_sevlet_with_logging.yml -e host=test_esiegl
 ansible-playbook pb_test_db_app.yml -e host=test_tester
```

oder mit allgemeinem Playbook:
```
ansible-playbook ../pb/PB_wildfly_install.yml -i ../../STAGES/CUST/PT/hosts -e host=CUST-PTEVAL-AUMKG -e group_id=at.test  -e artifact_id=servlet-with-logging -e version=1.1.0
```
