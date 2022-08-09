#!/bin/bash

bash scripts/clean.sh
bash scripts/build.sh
rm -rf metastore_db
rm -rf derby.log
mkdir -p data/input
cp -r test/test_data/input/* data/input/
. scripts/activate_venv.sh
bash scripts/create-db-test.sh
bash artifact/datamask-pyutil.sh artifact test/test_parms/test_parms.json "TestRent" "offset=4,offset=1" "-v -v"   
#bash artifact/datamask-pyutil.sh artifact test/test_parms/test_parms.json "TestUser" "offset=1" "-v -v"  
