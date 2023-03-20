# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import os
import json
from typing import cast
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,    
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_kms as kms
)
from constructs import Construct
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
        
class EmrProfileStack(Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        NAMING_PREFIX = os.environ["NAMING_PREFIX"]
        VPC_ID = ssm.StringParameter.value_from_lookup(self, f"/{NAMING_PREFIX}/vpc/id")
        
        glueSampleDb=cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-sample-db-export')

        #Get objects from the data lake stack
        artifacts_bucket = s3.Bucket.from_bucket_name(
            self, 'ArtifactsBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-artifact-bucket-export'))
        logs_bucket = s3.Bucket.from_bucket_name(
            self, 'LogsBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-logs-bucket-export'))    
        control_bucket = s3.Bucket.from_bucket_name(
            self, 'ControlBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-control-bucket-export'))
        landing_zone_bucket = s3.Bucket.from_bucket_name(
            self, 'LandingZoneBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-landing-bucket-export'))
        data_out_bucket = s3.Bucket.from_bucket_name(
            self, 'DataOutBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-dataout-bucket-export'))

        ###################################################################
        #
        # EMR Profile
        #
        ###################################################################

        kerberos_attributes_secret = secretsmanager.Secret(
            self, 'DatamaskKerberosAttributesSecret',
            secret_name=f'{NAMING_PREFIX}-kerberos-attributes',
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({
                    'Realm': 'EC2.INTERNAL',
                }),
                generate_string_key='KdcAdminPassword',
            ),
        ) 

        # Here we create a KMS Key to use for At Rest Encryption in S3 and Locally
        kms_key = kms.Key(self, 'AtRestKMSKey')
        vpc = ec2.Vpc.from_lookup(self, 'DmfDemoVpcImport', vpc_id=VPC_ID)
        
        datamask_profile = emr_profile.EMRProfile(
            self, 'DatamaskProfile',
            profile_name='datamask-profile',
            vpc=vpc,
            logs_bucket=logs_bucket,
            artifacts_bucket=artifacts_bucket
        )
        # Get data lake bucket kms key
        datalake_bucket_kms = kms.Key.from_key_arn(
            self,
            f"{NAMING_PREFIX}-datalake_kms_arn",
            cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-bucket-kms-arn-export')
        )

        # Authorize the profile for the Data Bucket and set the At Rest Encryption type
        datamask_profile \
            .authorize_input_key(datalake_bucket_kms) \
            .authorize_output_key(datalake_bucket_kms) \
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
        datamask_profile.roles.instance_role.add_to_policy(_glue_catalog_policy(self,glueSampleDb))

        # Emr 5.30.1 needs ingress on port 9443 in the service security group
        datamask_profile.security_groups.service_group.add_ingress_rule(
            datamask_profile.security_groups.master_group, 
            ec2.Port.tcp(9443)
        )

        # This prepares the project's bootstrap_source/ folder for deployment
        # We use the Artifacts bucket configured and authorized on the EMR Profile
        bootstrap_code = emr_code.Code.from_path(
            path='bootstrap_source',
            deployment_bucket=artifacts_bucket,
            deployment_prefix='datamask/bootstrap_source')

        # Define a Bootstrap Action using the bootstrap_source/ folder's deployment location
        bootstrap = emr_code.EMRBootstrapAction(
            name='InstallPythonPackages',
            path=f'{bootstrap_code.s3_path}/install_python_packages.sh',
            args=['boto3', 's3fs','jsonschema'],
            code=bootstrap_code)

        # Cluster Configurations that use InstanceGroups are deployed to a Private subnet
        subnet = vpc.private_subnets[0]
        #subnet_list = [ec2.Subnet.from_subnet_attributes(self, "Subnet", subnet_id=vpc. SUBNET_ID, availability_zone=SUBNET_AZ)]
        #subnet = vpc.select_subnets(subnets=subnet_list).subnets[0]

        # Load a SecretsManger Secret with secure RDS Metastore credentials
        external_metastore_secret = secretsmanager.Secret(
            self, 'DatamaskExternalMetastoreSecret',
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
            self, 'DatamaskClusterConfiguration',
            configuration_name='datamask-instance-group-cluster',
            use_glue_catalog=True,
            release_label='emr-6.6.0',
            subnet=subnet,
            bootstrap_actions=[bootstrap],
            core_instance_count=5,
            core_instance_type='m5.2xlarge',
            step_concurrency_level=10,
            secret_configurations={'hive-site': external_metastore_secret})


        ##############################################################################
        #
        # EMR Cluster Configuration
        #
        # Create a new State Machine to launch a cluster with the Basic configuration
        # Unless specifically indicated, fail to start if a cluster of the same name
        # is already running. Allow any parameter in the default override_interface to
        # be overwritten.
        #
        ##############################################################################

        launch_function = emr_launch_function.EMRLaunchFunction(
            self, 'DatamaskEmrLaunchFunction',
            launch_function_name='launch_cluster',
            namespace='datamask',
            cluster_configuration=cluster_config,
            emr_profile=datamask_profile,
            cluster_name='datamask-cluster',
            default_fail_if_cluster_running=True,
            allowed_cluster_config_overrides=cluster_config.override_interfaces['default'],
            cluster_tags=[cdk.Tag('EmrProfile', 'datamask-profile'),cdk.Tag('Name','datamask-emr')],
            wait_for_cluster_start=True)

def _glue_catalog_policy(scope: Construct, dbname) -> iam.PolicyDocument:
    stack = Stack.of(scope)
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
                    resource=f'database/default'
                ),
                stack.format_arn(
                    partition=stack.partition,
                    service='glue',
                    resource=f'database/{dbname}'
                ),
                stack.format_arn(
                    partition=stack.partition,
                    service='glue',
                    resource=f'table/{dbname}/*'
                )
            ]
        )

