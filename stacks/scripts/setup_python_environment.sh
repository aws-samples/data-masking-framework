#!/bin/bash
#set -x

# This script to be executed as root
#
#
sudo yum update -y
sudo yum install -y python3
sudo yum install -y python-pip
python3 -m pip install --upgrade pip
python3 -m pip install virtualenv
python3 -m pip install git-remote-codecommit

sudo yum install -y docker
sudo usermod -a -G docker ec2-user
id ec2-user

sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo systemctl status docker.service
docker version

sudo yum install -y nodejs npm
npm --version

npm install -g aws-cdk
if [ $? -ne 0 ]
then
    echo "=========================================================="
    echo "The above error on aws-cdk installation is safe to ignore."
    echo "=========================================================="
    npm update -g aws-cdk
fi

npm install -g npm@9.2.0

cdk version

sudo yum install -y git-all 

# clone git repo
# cd local repo
# python3 -m venv env
# source env/bin/activate
