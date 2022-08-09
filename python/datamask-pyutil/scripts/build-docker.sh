#!/bin/bash

BUILD=test

rm -rf artifact

docker build --build-arg build_var=$BUILD . -t datamask 

mkdir artifact

docker run -v `pwd`/artifact:/artifact datamask /bin/cp -r /datamask/artifact /



