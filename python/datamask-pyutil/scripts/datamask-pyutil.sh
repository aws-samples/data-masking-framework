#!/bin/bash

set -x


if [ $# -ne 4 ] && [ $# -ne 5 ] 
then
	if [ $# -eq 3 ]
	then
		PART_LIST=""
	else
		echo "Illegal number of parameters [$#]"
		exit 1
	fi
else
	PART_LIST=$4
fi

ARTIFACT_PREFIX=$1
CONFIG_PATH=$2
JOB_NAME=$3
DEBUG=$5

DRIVER="$ARTIFACT_PREFIX/driver.py"

SPARK_SUBMIT_OPTIONS="spark-submit"


ARGS="--config-path $CONFIG_PATH --job-name $JOB_NAME $DEBUG"

if ! [ -z $PART_LIST ]
then
	ARGS="--part-list $PART_LIST $ARGS"
fi

echo $ARTIFACT_PREFIX | grep "s3"
if [ $? -eq 0 ]
then
	# botocore does not work with zip,whls and python files
	PACKAGE=`aws s3 ls $ARTIFACT_PREFIX/spark-dist/ | awk '$0 !~ "^boto" && $0 !~ "pyspark" && $0 ~ ".*\.zip$" { print prefix $NF }' prefix=$ARTIFACT_PREFIX/spark-dist/`
else
	# botocore does not work with zip,whls and python files
	PACKAGE=`ls $ARTIFACT_PREFIX/spark-dist/ | awk '$0 !~ "^boto" && $0 !~ "pyspark" && $0 ~ ".*\.zip$" { print prefix $NF }' prefix=$ARTIFACT_PREFIX/spark-dist/`
fi

PYFILES=`echo $PACKAGE | tr -s ' ' ','`

JARS=""

if [ -z $JARS ]
then
	SUBMIT_JARS=""
else
	SUBMIT_JARS="--jars $JARS"
fi

$SPARK_SUBMIT_OPTIONS --py-files $PYFILES $SUBMIT_JARS $DRIVER $ARGS

