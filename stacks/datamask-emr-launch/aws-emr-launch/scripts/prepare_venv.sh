#!/bin/bash

. .venv/bin/activate
export PYTHONPATH=.venv/lib/python3*/site-packages
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install aws-emr-launch==1.4.0
