#!/bin/bash

. .venv/bin/activate
export PYTHONPATH=`ls -df .venv/lib/python3*/* | grep site-packages | sort -r | head -1`

