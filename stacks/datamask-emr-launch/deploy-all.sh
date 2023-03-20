#!/bin/bash

[ -z "$AWS_REGION" ] && export AWS_REGION="us-east-1"

read -p "Enter AWS target region [`echo $AWS_REGION `]: " INPUT_REGION

[ ! -z $INPUT_REGION ] && export AWS_REGION=$INPUT_REGION

export AWS_DEFAULT_REGION=$AWS_REGION   # Needed/will be used by AWS EMR Launch package

echo "Using region  : " $AWS_REGION

export AWS_ACCOUNT=`aws sts get-caller-identity --query "Account" --output text`
if [[ $AWS_ACCOUNT =~ ^[0-9]{12} ]]
then
  echo "Using account : " $AWS_ACCOUNT
else
  echo "Invalid credential/profile in local environment!"
  exit 1
fi

read -p "E-mail address for job result notification [your_email@domain.com]: " EMAIL_INPUT

if [ -z $EMAIL_INPUT ]
then
  echo "E-mail notification is skipped."
  export EMAIL_NOTIFICATION="your_email@domain.com"
else
  export EMAIL_NOTIFICATION=$EMAIL_INPUT
  if [[ $EMAIL_NOTIFICATION =~ ^[[:alnum:]._%+-]+@[[:alnum:].-]+\.[[:alpha:].]{2,4}$ ]]
  then
    echo "Job result notification e-mail address : " $EMAIL_NOTIFICATION
  else
    echo "Invalid format of e-mail address!"
  fi
fi

echo
read -p "Continue the deployment? [y/n]" REPLY
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Aborting the deployment...."
    exit 1
fi

echo "###################################################################################"
echo " Setting up python virtual environment"
echo -e "###################################################################################\n"

pushd python-env
. scripts/set_env_var.sh
bash scripts/create_venv.sh 
bash scripts/prepare_venv.sh 
popd 

echo "###################################################################################"
echo " Building pyspark artifact"
echo -e "###################################################################################\n"
. ./python-env/.venv/bin/activate
pushd build
bash ../python-env/scripts/build.sh
popd

echo "###################################################################################"
echo " Activating python virtual environment"
echo -e "###################################################################################\n"

export PYTHONPATH=./python-env/.venv/lib/python3*/site-packages

echo "###################################################################################"
echo " Bootstrapping CDK"
echo -e "###################################################################################\n"
cdk bootstrap aws://$AWS_ACCOUNT/$AWS_REGION

echo "###################################################################################"
echo " Deploying data lake infrastructure"
echo -e "###################################################################################\n"
pushd datalake 
bash deploy.sh
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo " Deploying EMR control_plane"
echo -e "###################################################################################\n"
pushd emr-launch/control_plane 
bash deploy.sh
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo " Deploying datamask EMR profile"
echo -e "###################################################################################\n"
pushd emr-launch/datamask_profiles
bash deploy.sh 
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo " Deploying datamasking resources"
echo -e "###################################################################################\n"
pushd datamask-launch 
bash deploy.sh 
RET=$?
popd
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

echo "###################################################################################"
echo " Generating data masking configuration file (config.json) from template."
echo " The config.json file will be in stacks/datamask-emr-launch/configuration directory"
echo -e "###################################################################################\n"
bash ./python-env/scripts/create_config_json.sh
RET=$?
if [ $RET -ne 0 ]
then
	echo "RET:$RET"
	exit 1
fi

# A step to do before using EMR service-linked role for the first time on an AWS account & region
# Reference: https://docs.aws.amazon.com/emr/latest/ManagementGuide/using-service-linked-roles.html

TMPOUT=emrtmp.out
aws iam create-service-linked-role --aws-service-name elasticmapreduce.amazonaws.com > $TMPOUT 2>&1
if [ $? -ne 0 ]
then
    grep "AWSServiceRoleForEMRCleanup has been taken" $TMPOUT >/dev/null 2>&1
    if [ $? -ne 0 ]
    then
        echo "Launch this command when using the EMR service for the first time in this account:"
        echo "aws iam create-service-linked-role --aws-service-name elasticmapreduce.amazonaws.com"
        echo "Visit below reference for a more detail instruction:"
        echo "https://docs.aws.amazon.com/emr/latest/ManagementGuide/using-service-linked-roles.html"
    fi
fi
rm -f $TMPOUT >/dev/null 2>&1

echo
echo "###################################################################################"
echo " Deployment completed."
echo -e "###################################################################################\n"
