#!/usr/bin/env python3

import os
import json
from typing import Mapping

from aws_cdk import (
    aws_s3 as s3,    
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_secretsmanager as secretsmanager,
    aws_sns as sns,
    aws_iam as iam,
    core
)

from aws_emr_launch.constructs.emr_constructs import emr_code
from aws_emr_launch.constructs.managed_configurations import (
    instance_group_configuration,
)
from aws_emr_launch.constructs.emr_constructs import (
    cluster_configuration,
    emr_profile
)
from aws_emr_launch.constructs.step_functions import (
    emr_launch_function
)

def _glue_catalog_policy(scope: core.Construct) -> iam.PolicyDocument:
    stack = core.Stack.of(scope)
    return iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'glue:CreateDatabase',
                'glue:UpdateDatabase',
                'glue:DeleteDatabase',
                'glue:GetDatabase',
                'glue:GetDatabases',
                'glue:CreateTable',
                'glue:UpdateTable',
                'glue:DeleteTable',
                'glue:GetTable',
                'glue:GetTables',
                'glue:GetTableVersions',
                'glue:CreatePartition',
                'glue:BatchCreatePartition',
                'glue:UpdatePartition',
                'glue:DeletePartition',
                'glue:BatchDeletePartition',
                'glue:GetPartition',
                'glue:GetPartitions',
                'glue:BatchGetPartition',
                'glue:CreateUserDefinedFunction',
                'glue:UpdateUserDefinedFunction',
                'glue:DeleteUserDefinedFunction',
                'glue:GetUserDefinedFunction',
                'glue:GetUserDefinedFunctions'
            ],
            resources=[
                stack.format_arn(
                    partition=stack.partition,
                    service='glue',
                    resource='catalog'
                ),
                stack.format_arn(
                    partition=stack.partition,
                    service='glue',
                    resource='database/default'
                )
            ]
        )

app = core.App()

#Change Region and account
stack = core.Stack(app, 'DatamaskEmrProfilesStack', env=core.Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"]))

#Get Parameters
NAMING_PREFIX = os.environ["NAMING_PREFIX"]
ARTIFACTS_BUCKET = os.environ["ARTIFACTS_BUCKET"]
LOGS_BUCKET = os.environ["LOGS_BUCKET"]
CONTROL_BUCKET = os.environ["CONTROL_BUCKET"]
LANDING_ZONE_BUCKET = os.environ["LANDING_ZONE_BUCKET"]
DATA_OUT_BUCKET = os.environ["DATA_OUT_BUCKET"]
VPC_ID = os.environ["VPC_ID"]
SUBNET_ID = os.environ["SUBNET_ID"]
SUBNET_AZ = os.environ["SUBNET_AZ"]

#Get enviroment objects
artifacts_bucket = s3.Bucket.from_bucket_name(
    stack, 'ArtifactsBucket', ARTIFACTS_BUCKET )
logs_bucket = s3.Bucket.from_bucket_name(
    stack, 'LogsBucket', LOGS_BUCKET)
control_bucket = s3.Bucket.from_bucket_name(
    stack, 'ControlBucket', CONTROL_BUCKET)
landing_zone_bucket = s3.Bucket.from_bucket_name(
    stack, 'LandingZoneBucket', LANDING_ZONE_BUCKET)
data_out_bucket = s3.Bucket.from_bucket_name(
    stack, 'DataOutBucket', DATA_OUT_BUCKET)
vpc = ec2.Vpc.from_lookup(stack, 'Vpc', vpc_id=VPC_ID)

###################################################################
#
# EMR Profile
#
kerberos_attributes_secret = secretsmanager.Secret(
    stack, 'DatamaskKerberosAttributesSecret',
    secret_name=f'{NAMING_PREFIX}-kerberos-attributes',
    generate_secret_string=secretsmanager.SecretStringGenerator(
        secret_string_template=json.dumps({
            'Realm': 'EC2.INTERNAL',
        }),
        generate_string_key='KdcAdminPassword',
    ),
) 

# Here we create a KMS Key to use for At Rest Encryption in S3 and Locally
kms_key = kms.Key(stack, 'AtRestKMSKey')

datamask_profile = emr_profile.EMRProfile(
    stack, 'DatamaskProfile',
    profile_name='datamask-profile',
    vpc=vpc,
    logs_bucket=logs_bucket,
    artifacts_bucket=artifacts_bucket
)

# Authorize the profile for the Data Bucket and set the At Rest Encryption type
datamask_profile \
    .authorize_input_bucket(data_out_bucket) \
    .authorize_output_bucket(data_out_bucket) \
    .authorize_input_bucket(control_bucket) \
    .authorize_output_bucket(control_bucket) \
    .authorize_input_bucket(landing_zone_bucket) \
    .authorize_output_bucket(landing_zone_bucket) \
    .set_s3_encryption(emr_profile.S3EncryptionMode.SSE_S3) \
    .set_local_disk_encryption(kms_key, ebs_encryption=True) \
    .set_local_kdc(kerberos_attributes_secret)

# Add policy to get rights on glue catalog
datamask_profile.roles.instance_role.add_to_policy(_glue_catalog_policy(stack))

# Emr 5.30.1 needs ingress on port 9443 in the service security group
datamask_profile.security_groups.service_group.add_ingress_rule(
    datamask_profile.security_groups.master_group, 
    ec2.Port.tcp(9443)
)

# This prepares the project's bootstrap_source/ folder for deployment
# We use the Artifacts bucket configured and authorized on the EMR Profile
bootstrap_code = emr_code.Code.from_path(
    path='./bootstrap_source',
    deployment_bucket=artifacts_bucket,
    deployment_prefix='datamask/bootstrap_source')

# Define a Bootstrap Action using the bootstrap_source/ folder's deployment location
bootstrap = emr_code.EMRBootstrapAction(
    name='InstallPythonPackages',
    path=f'{bootstrap_code.s3_path}/install_python_packages.sh',
    args=['boto3', 's3fs','jsonschema'],
    code=bootstrap_code)

# Cluster Configurations that use InstanceGroups are deployed to a Private subnet
#subnet = vpc.private_subnets[0]
subnet_list = [ ec2.Subnet.from_subnet_attributes(stack, "Subnet", subnet_id=SUBNET_ID, availability_zone=SUBNET_AZ)]
subnet = vpc.select_subnets(subnets=subnet_list).subnets[0]

# Load a SecretsManger Secret with secure RDS Metastore credentials
external_metastore_secret = secretsmanager.Secret(
    stack, 'DatamaskExternalMetastoreSecret',
    secret_name=f'{NAMING_PREFIX}-external-metastore',
    generate_secret_string=secretsmanager.SecretStringGenerator(
        secret_string_template=json.dumps({
            'javax.jdo.option.ConnectionURL': 'jdbc',
            'javax.jdo.option.ConnectionDriverName': 'mariaDB',
            'javax.jdo.option.ConnectionUserName': 'user',
        }),
        generate_string_key='javax.jdo.option.ConnectionPassword',
    ),
)
        
# Create a basic Cluster Configuration using InstanceGroups, the Subnet and Bootstrap
# Action defined above, the EMR Profile we loaded, and defaults defined in
# the InstanceGroupConfiguration
cluster_config = instance_group_configuration.InstanceGroupConfiguration(
    stack, 'DatamaskClusterConfiguration',
    configuration_name='datamask-instance-group-cluster',
    use_glue_catalog=True,
    release_label='emr-5.31.0',
    subnet=subnet,
    bootstrap_actions=[bootstrap],
    core_instance_count=5,
    core_instance_type='m5.2xlarge',
    step_concurrency_level=10,
    secret_configurations={'hive-site': external_metastore_secret})

#basic_cluster_config.add_spark_package('com.amazon.deequ:deequ:1.0.2')

#basic_cluster_config.add_spark_jars(
#    emr_code.Code.from_path(
#        path='./jars',
#        deployment_bucket=artifacts_bucket,
#        deployment_prefix='datamask/jars'),
#    emr_code.Code.files_in_path('./jars', '*.jar'))

# Here we create another Cluster Configuration using the same subnet, bootstrap, and
# EMR Profile while customizing the default Instance Type and Instance Count
#high_mem_cluster_config = instance_group_configuration.InstanceGroupConfiguration(
#    stack, 'HighMemClusterConfiguration',
#    configuration_name='high-mem-instance-group-cluster',
#    subnet=subnet,
#    bootstrap_actions=[bootstrap],
#    step_concurrency_level=5,
#    core_instance_type='r5.2xlarge',
#    core_instance_count=2)

####################################################################
#
# EMR Cluster Configuration
#
# Create a new State Machine to launch a cluster with the Basic configuration
# Unless specifically indicated, fail to start if a cluster of the same name
# is already running. Allow any parameter in the default override_interface to
# be overwritten.
launch_function = emr_launch_function.EMRLaunchFunction(
    stack, 'DatamaskEmrLaunchFunction',
    launch_function_name='launch_cluster',
    namespace='datamask',
    cluster_configuration=cluster_config,
    emr_profile=datamask_profile,
    cluster_name='datamask-cluster',
    default_fail_if_cluster_running=True,
    allowed_cluster_config_overrides=cluster_config.override_interfaces['default'],
    cluster_tags=[core.Tag('EmrProfile', 'datamask-profile'),core.Tag('Name','datamask-emr')],
    wait_for_cluster_start=True)

app.synth()
