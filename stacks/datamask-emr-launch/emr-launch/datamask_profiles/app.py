# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import os
import aws_cdk as cdk
from lib.emr_profile_stack import EmrProfileStack

app = cdk.App()

EmrProfileStack(
    app,
    "DmfDemoEmrProfile",
    env=cdk.Environment(account=os.getenv("AWS_ACCOUNT"), region=os.getenv("AWS_REGION"))
    )

app.synth()
