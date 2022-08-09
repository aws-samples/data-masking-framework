#!/bin/bash
TIME=`date +"%Y%m%d%H%M%S"`
aws s3 --recursive mv $1/spark-dist $1/spark-dist-$TIME
aws s3 cp --recursive artifact $1
