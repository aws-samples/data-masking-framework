#!/bin/bash

#cdk destroy --force
# cdk deploy --verbose --require-approval never
cdk deploy --require-approval never
exit $?
