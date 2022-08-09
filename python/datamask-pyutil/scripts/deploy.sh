#!/bin/bash

BUCKET_PATH="s3://$1/datamask"

bash scripts/create_venv.sh
bash scripts/prepare_venv.sh
bash scripts/clean.sh
bash scripts/build.sh
bash scripts/upload-s3.sh $BUCKET_PATH
