#!/bin/bash

if [  $# -ne 1 ] 
then    
	echo "Syntax error"
	echo "cmd [BUCKET]"
	exit 1
fi 

BUCKET_TEST=$1
BUCKET_TEST_PATH=s3://$BUCKET_TEST

ARTIFACT_PREFIX=$BUCKET_TEST_PATH/artifact
CONFIG_PATH=$BUCKET_TEST_PATH/test/test_parms/test_parms.json

## Upload artifact to bucket
aws s3 rm --recursive $ARTIFACT_PREFIX 
aws s3 cp --recursive artifact $ARTIFACT_PREFIX
#
##Copy test data to S3
aws s3 cp --recursive test/test_data/input $BUCKET_TEST_PATH/data/input
#
##Copy json parameters to S3
mkdir -p tmp
sed "s/\"data\//\"s3:\/\/$BUCKET_TEST\/data\//g" test/test_parms/test_parms.json | sed "s/\"test\//\"s3:\/\/$BUCKET_TEST\/test\//g" > tmp/test_parms.json 
aws s3 cp tmp/test_parms.json $CONFIG_PATH
#
##Copy salts to S3
aws s3 cp test/test_data/salts/salt1/salt1.json $BUCKET_TEST_PATH/test/test_data/salts/salt1/salt1.json

