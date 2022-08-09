#!/bin/bash

rm -rf dist/* spark-dist/* build/* jars/* 2> /dev/null 
python3 setup.py clean
