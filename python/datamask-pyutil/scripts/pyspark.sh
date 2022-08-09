#!/bin/bash

. scripts/activate_venv.sh

PYSPARK_PYTHON=`which python3` pyspark  $*

