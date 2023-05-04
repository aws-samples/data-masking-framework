# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

#!/usr/bin/env python3

import os
import aws_cdk as cdk
from aws_emr_launch import control_plane

app = cdk.App()
control_plane.ControlPlaneStack(
    app,
    "DmfDemoEmrControlPlane",
    env=cdk.Environment(account=os.getenv("AWS_ACCOUNT"), region=os.getenv("AWS_REGION"))
    )

app.synth()
