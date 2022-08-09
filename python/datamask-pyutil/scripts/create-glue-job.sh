#!/bin/bash

if [  $# -ne 2 ] 
then
	echo "Syntax error"
	echo "cmd [BUCKET] [GLUE_ROLE]"
	exit 1
fi

BUCKET_TEST=$1
ROLE=$2

GLUE_JOB_NAME=datamask
BUCKET_TEST_PATH=s3://$BUCKET_TEST

ARTIFACT_PREFIX=$BUCKET_TEST_PATH/artifact
CONFIG_PATH=$BUCKET_TEST_PATH/test/test_parms/test_parms.json
JOB_NAME=TestRent
DEBUG="-v -v"
PART_LIST="offset=1,offset=3,offset=5"

DRIVER="$ARTIFACT_PREFIX/driver.py"

ARGS=" { \"--config-path\": \"$CONFIG_PATH\""
ARGS="$ARGS, \"--job-name\": \"$JOB_NAME\""

if ! [ -z $PART_LIST ]
then
        ARGS="$ARGS, \"--part-list\": \"$PART_LIST\""
fi

ARGS="$ARGS, \"-v\": \"\" " 
ARGS="$ARGS, \"-v\": \"\" " 

echo $ARTIFACT_PREFIX | grep "s3"

PACKAGE=`aws s3 ls $ARTIFACT_PREFIX/spark-dist/ |  awk '{ print prefix $NF }' prefix=$ARTIFACT_PREFIX/spark-dist/`
PYFILES=`echo $PACKAGE | tr -s ' ' ','`

ARGS="$ARGS, \"--extra-py-files\": \"$PYFILES\""
ARGS="$ARGS, \"--enable-glue-datacatalog\": \"\""
ARGS="$ARGS, \"--is-glue-job\" : \"\" }"

aws glue create-job --name $GLUE_JOB_NAME \
	--role $ROLE \
	--command Name=glueetl,ScriptLocation=$DRIVER,PythonVersion=3 \
	--non-overridable-arguments "$ARGS" \
	--glue-version 2.0 \

	

