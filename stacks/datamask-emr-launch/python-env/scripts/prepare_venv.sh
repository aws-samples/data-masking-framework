#!/bin/bash

. .venv/bin/activate
export PYTHONPATH=.venv/lib/python3*/site-packages

.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 -m pip install --upgrade pip