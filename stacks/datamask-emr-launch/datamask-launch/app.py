# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import os
import aws_cdk as cdk
from lib.datamask_launch_stack import DatamaskLaunchStack

app = cdk.App()

DatamaskLaunchStack(
    app,
    "DmfDemoDatamaskLaunch",
    env=cdk.Environment(account=os.getenv("AWS_ACCOUNT"), region=os.getenv("AWS_REGION"))
    )

app.synth()
