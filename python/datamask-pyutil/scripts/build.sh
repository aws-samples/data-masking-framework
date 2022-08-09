#!/bin/bash

. .venv/bin/activate
pip install pip --upgrade
pip install wheel
python setup.py bdist_wheel

if ! [ -d spark-dist ] 
then
	mkdir spark-dist 
fi

if ! [ -d jars ] 
then
	mkdir jars 
fi

#generate requiriments wheels
mkdir tmp
cat requirements.txt | grep -v pyspark | grep -v boto > tmp/requirements.txt
cd dist  
pip wheel -r ../tmp/requirements.txt
cd ..

rm -rf artifact 
mkdir artifact
cp -r spark-dist artifact/

# botocore does not work with zip, whls and spark extrar files
ls ./dist/ | egrep .*\.whl | awk -F '.' 'BEGIN { OFS = "."} $0 !~ "^boto" {$NF="";print }' | while read file
do
	cp  dist/${file}whl artifact/spark-dist/${file}zip
done

cp src/datamask_pyutil/driver* artifact/
cp scripts/datamask-pyutil.sh artifact/
