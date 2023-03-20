# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import os
import aws_cdk as cdk
from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_ssm as ssm,
    aws_glue as glue
)

class DataLakeStack(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        NAMING_PREFIX = os.environ["NAMING_PREFIX"]
        VPC_CIDR = os.environ["VPC_CIDR"]

        s3_kms_key = create_kms_key(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-bucket-kms')
        artifact_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-artifact-bucket', s3_kms_key)
        auditlogs_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-auditlogs-bucket', s3_kms_key)
        logs_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-logs-bucket', s3_kms_key)
        control_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-control-bucket', s3_kms_key, auditlogs_bucket)
        landing_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-landing-bucket', s3_kms_key, auditlogs_bucket)
        data_out_bucket = create_bucket(self, f'{NAMING_PREFIX}-{self.account}-{self.region}-dataout-bucket', s3_kms_key, auditlogs_bucket)

        self.vpc = create_vpc(self, NAMING_PREFIX, VPC_CIDR)
        
        dmfSampleDb = glue.CfnDatabase(
            self, f"{NAMING_PREFIX}_dmf_sample_db",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(name="dmf_sample_db")
        )

        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-artifact-bucket-export',
            value=artifact_bucket.bucket_name,
            export_name=f'{NAMING_PREFIX}-{self.region}-artifact-bucket-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-logs-bucket-export',
            value=logs_bucket.bucket_name,
            export_name=f'{NAMING_PREFIX}-{self.region}-logs-bucket-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-control-bucket-export',
            value=control_bucket.bucket_name,
            export_name=f'{NAMING_PREFIX}-{self.region}-control-bucket-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-landing-bucket-export',
            value=landing_bucket.bucket_name,
            export_name=f'{NAMING_PREFIX}-{self.region}-landing-bucket-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-dataout-bucket-export',
            value=data_out_bucket.bucket_name,
            export_name=f'{NAMING_PREFIX}-{self.region}-dataout-bucket-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-vpc-id-export',
            value=self.vpc.vpc_id,
            export_name=f'{NAMING_PREFIX}-{self.region}-vpc-id-export'
        )
        vpc_id_export = ssm.StringParameter(
            self,
            f"{NAMING_PREFIX}-vpc-id-ssm",
            parameter_name=f"/{NAMING_PREFIX}/vpc/id",
            description="VPC ID created for DMF demo/workshop",
            string_value=self.vpc.vpc_id
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-sample-db-export',
            value=dmfSampleDb.database_input.name,
            export_name=f'{NAMING_PREFIX}-{self.region}-sample-db-export'
        )
        cdk.CfnOutput(
            self,
            f'{NAMING_PREFIX}-{self.region}-bucket-kms-arn-export',
            value=s3_kms_key.key_arn,
            export_name=f'{NAMING_PREFIX}-{self.region}-bucket-kms-arn-export'
        )

def create_bucket(self, bucket_name, bucket_kms, audit_bucket = 'none') -> s3.Bucket:
        """
        Creates an Amazon S3 bucket to store data files. It attaches bucket policy with necessary guardrails.
        It enables server-side encryption using provided KMS key and leverage S3 bucket key feature.

        @param scope
        @param bucket_name str: The name for the bucket resource
        @param data_kms_key kms.Key: The KMS Key to use for encryption of data at rest

        @return: The bucket that was created
        """

        if audit_bucket == 'none':
            return s3.Bucket(
                self,
                id=bucket_name,
                access_control=s3.BucketAccessControl.LOG_DELIVERY_WRITE,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                bucket_name=bucket_name,
                encryption=s3.BucketEncryption.S3_MANAGED,
                public_read_access=False,
                removal_policy=cdk.RemovalPolicy.DESTROY,  # For the demo/workshop purpose
                versioned=True,
                enforce_ssl=True
            )
        else:
            return s3.Bucket(
                self,
                id=bucket_name,
                access_control=s3.BucketAccessControl.PRIVATE,
                server_access_logs_bucket=audit_bucket,
                server_access_logs_prefix=bucket_name,
                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                bucket_name=bucket_name,
                encryption=s3.BucketEncryption.KMS,
                encryption_key=bucket_kms,
                public_read_access=False,
                removal_policy=cdk.RemovalPolicy.DESTROY,  # For the demo/workshop purpose
                versioned=True,
                enforce_ssl=True
            )

def create_kms_key(self, name_prefix) -> kms.Key:
        """
        Creates an AWS KMS Key and attaches a Key policy

        @param deployment_account_id: The id for the deployment account
        @param logical_id str: The logical id prefix to apply to all CloudFormation resources
        @param resource_name_prefix: The resource name prefix to apply to all resource names
        """
        s3_kms_key = kms.Key(
            self,
            f'{name_prefix}KmsKey',
            admins=[iam.AccountPrincipal(self.account)],  # Gives account users admin access to the key
            description='Key used for encrypting Data Lake S3 Buckets',
            removal_policy=cdk.RemovalPolicy.DESTROY,  # For the demo/workshop purpose
            alias=f'{name_prefix}-kms-key'
        )
        # Gives account users and deployment account users access to use the key
        s3_kms_key.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[
                    iam.AccountPrincipal(self.account),
                ],
                actions=[
                    'kms:Encrypt',
                    'kms:Decrypt',
                    'kms:ReEncrypt*',
                    'kms:GenerateDataKey*',
                    'kms:DescribeKey',
                ],
                resources=["*"],
            )
        )
        return s3_kms_key

def create_vpc(self, name_prefix, vpc_cidr) -> ec2.Vpc:
        vpc = ec2.Vpc(
            self,
            f'{name_prefix}Vpc',
            ip_addresses=ec2.IpAddresses.cidr(vpc_cidr),
            vpc_name=f"{name_prefix}-vpc",
            max_azs=1,
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
        shared_security_group_ingress = ec2.SecurityGroup(
            self,
            f'{name_prefix}SharedIngressSecurityGroup',
            vpc=vpc,
            description='Shared Security Group for Data Lake resources with self-referencing ingress rule.',
            security_group_name=f'{name_prefix}SharedIngressSecurityGroup',
        )
        shared_security_group_ingress.add_ingress_rule(
            peer=shared_security_group_ingress,
            connection=ec2.Port.all_traffic(),
            description='Self-referencing ingress rule',
        )
        vpc.add_gateway_endpoint(
            f'{name_prefix}S3Endpoint',
            service=ec2.GatewayVpcEndpointAwsService.S3
        )
        vpc.add_interface_endpoint(
            f'{name_prefix}KmsEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService.KMS,
            security_groups=[shared_security_group_ingress],
        )
        return vpc