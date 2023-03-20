#!/bin/bash

TEMPLATE_FILE=configuration/template-config.json
CONFIG_FILE=configuration/config.json

cp $TEMPLATE_FILE $CONFIG_FILE

sed -i -E "s/NAMING_PREFIX/${NAMING_PREFIX}/; s/AWS_ACCOUNT/${AWS_ACCOUNT}/; s/AWS_REGION/${AWS_REGION}/" $CONFIG_FILE
