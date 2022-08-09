#!/bin/bash

#export NAMING_PREFIX="${PREFIX}${ENV}-datamask"
#export VPC_ID="$VPC"
#export SUBNET_ID="$SUBNET"
#export SUBNET_AZ="$AZ"
#export LOGS_BUCKET="${PREFIX}${ENV}-logs"
#export LANDING_ZONE_BUCKET="${PREFIX}${ENV}-landing"
#export ARTIFACTS_BUCKET="${PREFIX}${ENV}-artifact"
#export CONTROL_BUCKET="${PREFIX}${ENV}-datamask"
#export DATA_OUT_BUCKET="${PREFIX}${ENV}-ingestion"

if [ -z "$NAMING_PREFIX" ]
then
	echo "Environment variable NAMING_PREFIX needed"
	exit 1
fi
if [ -z "$VPC_ID" ]
then
	echo "Environment variable VPC_ID needed"
	exit 1
fi
if [ -z "$SUBNET_ID" ]
then
	echo "Environment variable SUBNET_ID needed"
	exit 1
fi
if [ -z "$SUBNET_AZ" ]
then
	echo "Environment variable SUBNET_AZ needed"
	exit 1
fi
if [ -z "$LOGS_BUCKET" ]
then
	echo "Environment variable LOGS_BUCKET needed"
	exit 1
fi
if [ -z "$LANDING_ZONE_BUCKET" ]
then
	echo "Environment variable LANDING_ZONE_BUCKET needed"
	exit 1
fi
if [ -z "$ARTIFACTS_BUCKET" ]
then
	echo "Environment variable ARTIFACTS_BUCKET needed"
	exit 1
fi
if [ -z "$CONTROL_BUCKET" ]
then
	echo "Environment variable CONTROL_BUCKET needed"
	exit 1
fi
if [ -z "$DATA_OUT_BUCKET" ]
then
	echo "Environment variable DATA_OUT_BUCKET needed"
	exit 1
fi

#cdk diff 
cdk deploy --require-approval never 
exit $?
