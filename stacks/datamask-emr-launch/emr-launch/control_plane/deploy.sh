#!/bin/bash

#cdk diff
cdk deploy  --require-approval never
exit $?
