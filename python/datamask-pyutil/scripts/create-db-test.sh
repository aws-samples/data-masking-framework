#!/bin/bash

echo "Creating test DB"
mkdir ./tmp 2> /dev/null

PWD=`pwd`
echo "PWD: $PWD"

echo "
from pyspark.sql import SparkSession
if __name__ == '__main__':
   print('Creating test DB')
   spark = SparkSession.builder.appName('CreateDB').enableHiveSupport().config('spark.sql.warehouse.dir', 'file://$PWD').getOrCreate()
   spark.sql('create database db1')
   spark.stop()
" > ./tmp/create_db.py

export PYSPARK_PYTHON=`which python3`

spark-submit ./tmp/create_db.py

