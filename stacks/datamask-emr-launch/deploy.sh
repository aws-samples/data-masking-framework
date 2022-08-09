#!/bin/bash

#CHANGE THE VARIABLES RELATED TO CORRECT ENVIRONMENT
#PREFIX="dmask-"
#ENV="dev"
#ARTF_PARAM_FILE="config.json"
#VPC="vpc-id"
#SUBNET="subnet-id"
#AZ="us-east-1a"

if [ -z $PREFIX ]
then
    echo "Variable PREFIX is needed"
    exit 1
fi

if [ -z $ENV ]
then
    echo "Variable ENV is needed"
    exit 1
fi

if [ -z $ARTF_PARAM_FILE ]
then
    echo "Variable ARTF_PARAM_FILE is needed"
    exit 1
fi

if [ -z $VPC ]
then
    echo "Variable VPC is needed"
    exit 1
fi
if [ -z $SUBNET ]
then
    echo "Variable SUBNET is needed"
    exit 1
fi
if [ -z $AZ ]
then
    echo "Variable AZ is needed"
    exit 1
fi

export NAMING_PREFIX="${PREFIX}${ENV}-datamask"
export VPC_ID="$VPC"
export SUBNET_ID="$SUBNET"
export SUBNET_AZ="$AZ"
export LOGS_BUCKET="${PREFIX}${ENV}-logs"
export LANDING_ZONE_BUCKET="${PREFIX}${ENV}-landing"
export ARTIFACTS_BUCKET="${PREFIX}${ENV}-artifact"
export CONTROL_BUCKET="${PREFIX}${ENV}-datamask"
export DATA_OUT_BUCKET="${PREFIX}${ENV}-ingestion"
export CONFIG_PATH="s3://$ARTIFACTS_BUCKET/datamask/${ARTF_PARAM_FILE}"
export TABLE_PREFIX_RE='[^/]*/[^/]*'
export FILE_EXCLUDE_RE='^__|^\.|/__|/\.'
export FILE_INCLUDE_RE='\.parquet$|\.csv$'
export CRON_DAY='*'
export CRON_WEEK_DAY='*'
export CRON_MINUTE='0'
export CRON_HOUR='0'

echo "###################################################################################"
echo "Setup python virtual env"
echo "###################################################################################"
pushd aws-emr-launch 
bash scripts/create_venv.sh 
bash scripts/prepare_venv.sh 
popd 

echo "###################################################################################"
echo "Activate virtual env"
echo "###################################################################################"
. ./aws-emr-launch/.venv/bin/activate
export PYTHONPATH=./aws-emr-launch/.venv/lib/python3*/site-packages


echo "###################################################################################"
echo "Bootstrap CDK"
echo "###################################################################################"
cdk bootstrap aws://$AWS_ACCOUNT/$AWS_REGION

echo "###################################################################################"
echo "Deploy control_plane"
echo "###################################################################################"
pushd emr-launch/control_plane 
bash deploy.sh 
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo "Deploy datamask emr profile"
echo "###################################################################################"
pushd emr-launch/profiles/datamask-emr-profile 
bash deploy.sh 
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo "Deploy datamask launch"
echo "###################################################################################"
pushd datamask-launch 
bash deploy.sh 
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

