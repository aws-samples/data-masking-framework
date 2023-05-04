#!/bin/bash

#export NAMING_PREFIX="${PREFIX}${ENV}-datamask"
#export ARTIFACTS_BUCKET="${PREFIX}${ENV}-artifact"
#export LANDING_ZONE_BUCKET="${PREFIX}${ENV}-landing"
#export CONFIG_PATH="s3://$ARTIFACTS_BUCKET/datamask/poc_parms.json"
#export TABLE_PREFIX_RE='[^/]*R/[^/]*'
#export FILE_EXCLUDE_RE='^__|^\.|/__|/\.'
#export FILE_INCLUDE_RE=='\.parquet$|\.csv$'

if [ -z "$NAMING_PREFIX" ]
then
	echo "Environment variable NAMING_PREFIX is needed"
	exit 1
fi

if [ -z "$TABLE_PREFIX_RE" ]
then
	echo "Environment variable TABLE_PREFIX_RE is needed"
	exit 1
fi

if [ -z "$FILE_EXCLUDE_RE" ]
then
	echo "Environment variable FILE_EXCLUDE_RE is needed"
	exit 1
fi

if [ -z "$FILE_INCLUDE_RE" ]
then
	echo "Environment variable FILE_INCLUDE_RE is needed"
	exit 1
fi

if [ -z "$CRON_HOUR" ]
then
	echo "Environment variable CRON_HOUR is needed"
	exit 1
fi

if [ -z "$CRON_DAY" ]
then
	echo "Environment variable CRON_DAY is needed"
	exit 1
fi

if [ -z "$CRON_MINUTE" ]
then
	echo "Environment variable CRON_MINUTE is needed"
	exit 1
fi

if [ -z "$CRON_WEEK_DAY" ]
then
	echo "Environment variable CRON_WEEK_DAY is needed"
	exit 1
fi

#cdk deploy --verbose --require-approval never
cdk deploy --require-approval never
exit $?