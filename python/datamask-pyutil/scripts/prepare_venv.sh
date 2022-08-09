#!/bin/bash


#. .venv/bin/activate
. .venv/bin/activate
export PYTHONPATH=`ls -df .venv/lib/python3*/* | grep site-packages | sort -r | head -1`
.venv/bin/pip install --upgrade pip wheel
.venv/bin/pip install -r requirements.txt
