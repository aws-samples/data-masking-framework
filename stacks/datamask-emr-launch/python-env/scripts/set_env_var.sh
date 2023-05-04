#!/bin/bash

export NAMING_PREFIX="dmfsample"
export VPC_CIDR="10.30.0.0/16"
export ARTIFACT_PARAM_FILE="datamask/config.json"
export TABLE_PREFIX_RE="[^/]*/[^/]*"
export FILE_EXCLUDE_RE="^__|^\.|/__|/\."
export FILE_INCLUDE_RE="\.parquet$|\.csv$"
export CRON_DAY="*"
export CRON_WEEK_DAY="*"
export CRON_MINUTE="0"
export CRON_HOUR="0"