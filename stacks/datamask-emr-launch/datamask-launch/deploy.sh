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
	echo "Environment variable NAMING_PREFIX needed"
	exit 1
fi

if [ -z "$ARTIFACTS_BUCKET" ]
then
	echo "Environment variable ARTIFACTS_BUCKET needed"
	exit 1
fi

if [ -z "$LANDING_ZONE_BUCKET" ]
then
	echo "Environment variable LANDING_ZONE_BUCKET needed"
	exit 1
fi

if [ -z "$CONFIG_PATH" ]

then
	echo "Environment variable CONFIG_PATH needed"
	exit 1
fi

if [ -z "$TABLE_PREFIX_RE" ]
then
	echo "Environment variable TABLE_PREFIX_RE needed"
	exit 1
fi

if [ -z "$FILE_EXCLUDE_RE" ]
then
	echo "Environment variable FILE_EXCLUDE_RE needed"
	exit 1
fi

if [ -z "$FILE_INCLUDE_RE" ]
then
	echo "Environment variable FILE_INCLUDE_RE needed"
	exit 1
fi

if [ -z "$CRON_HOUR" ]
then
	echo "Environment variable CRON_HOUR needed"
	exit 1
fi

if [ -z "$CRON_DAY" ]
then
	echo "Environment variable CRON_DAY needed"
	exit 1
fi

if [ -z "$CRON_MINUTE" ]
then
	echo "Environment variable CRON_MINUTE needed"
	exit 1
fi

if [ -z "$CRON_WEEK_DAY" ]
then
	echo "Environment variable CRON_WEEK_DAY needed"
	exit 1
fi

#cdk diff
cdk deploy  --require-approval never
exit $?
