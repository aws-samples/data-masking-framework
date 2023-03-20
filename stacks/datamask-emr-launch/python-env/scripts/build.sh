#!/bin/bash
# By design this will be executed from within the build subdirectory

cp -R ../../../python/datamask-pyutil/src .

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
cp ../../../python/datamask-pyutil/scripts/datamask-pyutil.sh artifact/
cp -R artifact/* ../artifact
cp -R ../emr-launch/datamask_profiles/bootstrap_source ../artifact
# rm -fr tmp src artifact spark-dist jars dist build