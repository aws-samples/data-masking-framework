# Datamsk EMR launch 

*Deploy datamask-pyutil using EMR launch*

## Table of contents

- [Quick Start](#quick-start) 

## Quick Start
### Pyspark + EMR/GLUE

Deploy datamask-pyutil to run with pyspark in a S3 bucket.
```
$ git clone [REPOSITORY PATH]
$ cd datamask-pyutil
$ bash scripts/deploy.sh [BUCKET TO DEPLOY] 

```
   The folder ./artfact will be created on the build process and it will be uploaded on [BUCKET TO DEPLOY]
   Than use the artifacts to run a EMR step or a GLUE job.
   The script entry point will be on "s3::/[BUCKET]/datamask/datamask-pyutil.sh"


### Custom Pyspark   

Create you own pyspark module with the conf_process class.

First import and build artifacts files to be included in the spark-submit execution: 
```
$ git clone [REPOSITORY PATH]
$ cd datamask-pyutil
$ bash scripts/build.sh [BUCKET TO DEPLOY] 
```
Create your own pyspark script following the example above:

```
from datamask_pyutil import conf_process

''' 
Initialize the Spark context 
'''
jobname='JobName'
part_vet=['ano=2020','month=12']

cf = conf_process.DatamaskConfProcess(configPath, jobName)

if not cf.is_job_active():
    print("Jobname[{}] is not active".format(jobName))
else:
  cf.process_spark(part_vet, spark)

```
Than call spark-submit with all files in "./artifacts/spark-dist/*" in the "--py-files"

### Local test

You can use "artifact/datamask-pyutil.sh" to run a local environment of pyspark also.
Use scripts/run-test.sh as a example. 
Test case:
- ./test/test_data/input: test input data
- ./test/test_data/salts: test salts
- ./test/test_parms/test_parms.json: test parameters

### Parameters

All the parameters are stored in a JSON file with the following schema:

See [datamask.schema.md](./datamask-pyutil/schemas/datamask.schema.md)

