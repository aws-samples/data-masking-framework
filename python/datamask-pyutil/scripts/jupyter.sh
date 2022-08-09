#!/bin/bash

. scripts/activate_venv.sh
.venv/bin/pip install jupyter sparksql-magic
PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" PYSPARK_PYTHON=/usr/local/bin/python3 $PYTHONPATH/pyspark/bin/pyspark  $*

