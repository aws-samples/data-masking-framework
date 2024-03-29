# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import os, uuid

import aws_cdk as cdk
from aws_cdk import (
    App, Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfnt,
    aws_events as ev,
    aws_events_targets as evt,
    aws_lambda as lbd,
    aws_iam as iam,
    aws_dynamodb as ddb,
    custom_resources as cr
)
from constructs import Construct

from aws_emr_launch.constructs.emr_constructs import (
    emr_code
)
from aws_emr_launch.constructs.step_functions import (
    emr_launch_function,
    emr_chains,
    emr_tasks
)
from aws_emr_launch.constructs.lambdas import emr_lambdas
from typing import List, Optional

class _AddStepWithArgumentOverrides(sfn.StateMachineFragment):
    def __init__(self, scope: Construct, id: str, *,
                 emr_step: emr_code.EMRStep,
                 cluster_id: str,
                 result_path: Optional[str] = None,
                 output_path: Optional[str] = None,
                 fail_chain: Optional[sfn.IChainable] = None,
                 wait_for_step_completion: bool = True,
                 execution_input: Optional[str] = None,
                 interval_retry = None,
                 max_attempts_retry = None):
        super().__init__(scope, id)

        override_step_args = emr_lambdas.OverrideStepArgsBuilder.get_or_build(self)

        if not execution_input:  
            execution_input = sfn.TaskInput.from_json_path_at('$$.Execution.Input').value

        override_step_args_task = sfnt.LambdaInvoke(
            self, f'{emr_step.name} - Override Args',
            result_path=f'$.{id}ResultArgs',
            lambda_function=override_step_args,
            payload_response_only=True,
            payload=sfn.TaskInput.from_object({
                    'ExecutionInput': execution_input,
                    'StepName': emr_step.name,
                    'Args': emr_step.args
                })
        )

        resolved_step = emr_step.resolve(self)
        resolved_step['HadoopJarStep']['Args'] = sfn.TaskInput.from_json_path_at(f'$.{id}ResultArgs').value

        # integration_pattern = sfn.ServiceIntegrationPattern.SYNC if wait_for_step_completion \
        #     else sfn.ServiceIntegrationPattern.FIRE_AND_FORGET
        integration_pattern = (
            sfn.IntegrationPattern.RUN_JOB if wait_for_step_completion else sfn.IntegrationPattern.REQUEST_RESPONSE
        )

        add_step_task = emr_tasks.EmrAddStepTask(
            self,
            emr_step.name,
            output_path=output_path,
            result_path=result_path,
            cluster_id=cluster_id,
            step=resolved_step,
            integration_pattern=integration_pattern,
        )

        if interval_retry:
            add_step_task.add_retry(interval=interval_retry, max_attempts=max_attempts_retry)

        if fail_chain:
            override_step_args_task.add_catch(fail_chain, errors=['States.ALL'], result_path='$.Error')
            add_step_task.add_catch(fail_chain, errors=['States.ALL'], result_path='$.Error')

        override_step_args_task.next(add_step_task)

        self._start = override_step_args_task
        self._end = add_step_task

    @property
    def start_state(self) -> sfn.State:
        return self._start

    @property
    def end_states(self) -> List[sfn.INextable]:
        return self._end.end_states

class DatamaskLaunchStack(Stack):

    def __init__(self, scope: App, construct_id: str, **kwargs) -> None:        
        super().__init__(scope, construct_id, **kwargs)

        NAMING_PREFIX = os.environ["NAMING_PREFIX"]
        ARTIFACT_PARAM_FILE = os.environ["ARTIFACT_PARAM_FILE"]
        TABLE_PREFIX_RE = os.environ["TABLE_PREFIX_RE"]
        FILE_EXCLUDE_RE = os.environ["FILE_EXCLUDE_RE"]
        FILE_INCLUDE_RE = os.environ["FILE_INCLUDE_RE"]
        CRON_DAY = os.environ["CRON_DAY"]
        CRON_WEEK_DAY = os.environ["CRON_WEEK_DAY"]
        CRON_MINUTE = os.environ["CRON_MINUTE"]
        CRON_HOUR = os.environ["CRON_HOUR"]
        EMAIL_NOTIFICATION = os.environ["EMAIL_NOTIFICATION"]

        ######################################################################################
        ##  Queues 
        ######################################################################################
        queue_s3_events = sqs.Queue(self, "SQSQueueS3Events",queue_name=f'{NAMING_PREFIX}-queue-s3-events',retention_period=cdk.Duration.days(14))
        queue_job_ready = sqs.Queue(self, "SQSQueueJobReady",queue_name=f'{NAMING_PREFIX}-queue-job-ready',retention_period=cdk.Duration.days(14))


        ######################################################################################
        ##  Buckets
        ######################################################################################

        #Get objects from the data lake stack
        artifacts_bucket = s3.Bucket.from_bucket_name(
            self, 'ArtifactsBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-artifact-bucket-export'))
        landing_zone_bucket = s3.Bucket.from_bucket_name(
            self, 'LandingZoneBucketImport', cdk.Fn.import_value(f'{NAMING_PREFIX}-{self.region}-landing-bucket-export'))

        CONFIG_PATH = f's3://{artifacts_bucket.bucket_name}/{ARTIFACT_PARAM_FILE}'

        # Deploy pyspark artifacts
        artifact_deployment = s3_deployment.BucketDeployment(
            self,
            f"{NAMING_PREFIX}-DeployDatamaskFrameworkArtifacts",
            sources=[s3_deployment.Source.asset('../artifact')],   # path relative to the app.py of datamask launch app
            destination_bucket=artifacts_bucket,
            destination_key_prefix='datamask'
        )

        #landing_zone_bucket.add_event_notification(s3.EventType.OBJECT_CREATED,s3n.SqsDestination(queue_s3_events))
        notification_resource = cr.AwsCustomResource(self, 
                'S3NotificationResource',
                policy=cr.AwsCustomResourcePolicy.from_statements(
                    [
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE, #['*'],
                            actions=['s3:PutBucketNotification']
                        )
                    ]
                ),
                on_create=cr.AwsSdkCall(
                    service="S3",
                    action="putBucketNotificationConfiguration",
                    parameters={
                        "Bucket": landing_zone_bucket.bucket_name,
                        "NotificationConfiguration": {
                            "QueueConfigurations": [
                                {
                                    "Events": [
                                        's3:ObjectCreated:*'],
                                    "QueueArn": queue_s3_events.queue_arn
                                }
                            ]
                        }
                    },
                    physical_resource_id=cr.PhysicalResourceId.of(
                        f's3-notification-resource-{str(uuid.uuid1())}'),
                    region=self.region
                ),
                on_delete=cr.AwsSdkCall(
                    service="S3",
                    action="putBucketNotificationConfiguration",
                    parameters={
                        "Bucket": landing_zone_bucket.bucket_name,
                        "NotificationConfiguration": {
                        }
                    },
                    physical_resource_id=cr.PhysicalResourceId.of(
                        f's3-notification-resource-{str(uuid.uuid1())}'),
                    region=self.region
                )
                )

        queue_s3_events.add_to_resource_policy(iam.PolicyStatement(
            principals=[iam.ServicePrincipal("s3.amazonaws.com")],
            actions=["SQS:SendMessage"],
            resources=[queue_s3_events.queue_arn],
            conditions={
                "ArnEquals":
                    {"aws:SourceArn": landing_zone_bucket.bucket_arn}
                    }
            )
            )

        notification_resource.node.add_dependency(landing_zone_bucket)
        notification_resource.node.add_dependency(queue_s3_events)


        ######################################################################################
        ## Jobs Table
        ######################################################################################
        jobs_table = ddb.Table(
                    self, "datamask_jobs_table",
                    table_name=f'{NAMING_PREFIX}-jobs',
                    partition_key=ddb.Attribute(
                        name="id",
                        type=ddb.AttributeType.STRING
                    ),
                    removal_policy=cdk.RemovalPolicy.DESTROY
                )


        ######################################################################################
        #Pipeline Topics
        ######################################################################################

        success_topic = sns.Topic(self, 'PipelineSuccessTopic',topic_name=f'{NAMING_PREFIX}-pipeline-success')
        failure_topic = sns.Topic(self, 'PipelineFailureTopic',topic_name=f'{NAMING_PREFIX}-pipeline-failed')

        success_topic_subscriber = sns.Subscription(self,
            f'{NAMING_PREFIX}PipelineRunSuccessNotificationSubscriber',
            topic=success_topic,
            protocol=sns.SubscriptionProtocol("EMAIL"),
            endpoint=EMAIL_NOTIFICATION
        )
        failure_topic_subscriber = sns.Subscription(self,
            f'{NAMING_PREFIX}PipelineRunFailureNotificationSubscriber',
            topic=failure_topic,
            protocol=sns.SubscriptionProtocol("EMAIL"),
            endpoint=EMAIL_NOTIFICATION
        )
        ######################################################################################
        # DATAMASK_PIPELINE STEP FUNCTION
        ######################################################################################

        # Use the Launch Cluster State Machine we created in the emr_launch_function example
        launch_function = emr_launch_function.EMRLaunchFunction.from_stored_function(
                self, 'BasicLaunchFunction', 'launch_cluster', namespace='datamask')

        # Prepare the scripts executed by our Steps for deployment
        # This uses the Artifacts bucket defined in Cluster Configuration used by our
        # Launch Function
        #step_code = emr_code.Code.from_path(
        #    path='./step_sources',
        #    deployment_bucket=artifact_bucket,
        #    deployment_prefix='datamask/step_sources')

        ## FAIL  CHAIN
        # Create a Chain to receive Failure messages
        fail = emr_chains.Fail(
            self, 'FailChain',
            message=sfn.TaskInput.from_json_path_at('$.Error'),
            subject='Pipeline Failure',
            topic=failure_topic)
        # Define a Task to Terminate the Cluster on failure
        terminate_failed_cluster = emr_tasks.TerminateClusterBuilder.build(
            self, 'TerminateFailedCluster',
            name='Terminate Failed Cluster',
            cluster_id=sfn.TaskInput.from_json_path_at('$.ClusterId').value,
            result_path='$.TerminateResult').add_catch(fail, errors=['States.ALL'], result_path='$.Error')
        # Desisioin to choice if launch the cluster or not
        terminate_failed_choice = sfn.Choice(
                    self, 
                    "Decision Terminate Failure",
                    comment="Terminate on Failure?"
                )
        #Terminate failed choice
        #terminate_failed_choice.when(sfn.Condition.string_equals("$.ClusterId",""),terminate_failed_cluster.next(fail)).otherwise(fail)
        terminate_failed_choice.when(sfn.Condition.string_equals("$.Launched","1"),terminate_failed_cluster.next(fail)).otherwise(fail)

        ## CHECK MESSAGES
        # Define the task for lambda function to check if there are messages in the queuee 
        lambda_check_messages = lbd.Function(
                    self, 'LambdaFunctionCheckMessages',
                    handler='lambda_function.lambda_handler',
                    code=lbd.Code.from_asset("lambda_sources/check_messages"),
                    runtime=lbd.Runtime.PYTHON_3_7,
                    timeout=cdk.Duration.seconds(300),
                    environment={
                        'QUEUE_URL': queue_job_ready.queue_url
                    }
                )
        queue_job_ready.grant_consume_messages(lambda_check_messages)
        check_messages_task = sfnt.LambdaInvoke(
                self,
                "Check Messages SQS",
                lambda_function=lambda_check_messages,
                result_path="$.CheckMessagesSQSResult",
                #parameters={"Tag": "ClusterId","Value.$": "$$.Execution.Input.ClusterId"},
                comment="Check Messages from SQS",
                payload_response_only=True
                )
        # Desision to choice if there are messages or not        
        check_messages_choice = sfn.Choice(
                    self, 
                    "Decision Check Messages SQS",
                    comment="Are there messages to process?"
                )

        ## LAUNCH CLUSTER
        # Usie the State Machine defined earlier to launch the Cluster
        # The ClusterConfigurationOverrides and Tags will be passed through for
        # runtime overrides
        # Desision to choice if launch the cluster or not
        launch_cluster_choice = sfn.Choice(
                    self, 
                    "Decision Launch Cluster",
                    comment="Are there ClusterId in the Execution Input"
                )
        launch_cluster = emr_chains.NestedStateMachine(
            self, 'LaunchCluster',
            name='Launch Cluster',
            state_machine=launch_function.state_machine,
            fail_chain=fail)

        ##READ MESSAGES CHAIN
        #Passing corrent ClusterID
        pass_cluster_id_execution_to_read = sfn.Pass(
                self,
                "Pass Execution Cluster Id to Read",
                comment="Pass Execution Cluster Id to Read",
                result_path="$.PassClusterIdReadResult",
                output_path="$.PassClusterIdReadResult",
                parameters={
                    "ClusterId.$": "$$.Execution.Input.ClusterId",
                    "Launhced": "0"
                }
                )
        pass_cluster_id_launched_to_read = sfn.Pass(
                self,
                "Pass Launched  Cluster Id to Read",
                comment="Pass Cluster Id to Read",
                result_path="$.PassClusterIdReadResult",
                output_path="$.PassClusterIdReadResult",
                parameters={
                    "ClusterId.$": "$.LaunchClusterResult.ClusterId",
                    "Launched": "1"
                }
                )
        #Define the task fro the lambda function to receive all the messages
        lambda_read_messages = lbd.Function(
                    self, 'LambdaFunctionReadMessages',
                    handler='lambda_function.lambda_handler',
                    code=lbd.Code.from_asset("lambda_sources/receive_messages"),
                    runtime=lbd.Runtime.PYTHON_3_7,
                    timeout=cdk.Duration.seconds(300),
                    environment={
                        'QUEUE_URL': queue_job_ready.queue_url
                    }
                )
        queue_job_ready.grant_consume_messages(lambda_read_messages)
        read_messages_task= sfnt.LambdaInvoke(
                self,
                "Read Messages SQS",
                lambda_function=lambda_read_messages,
                payload=sfn.TaskInput.from_object({"Tag": "ClusterId","Value.$": "$.ClusterId"}),
                result_path="$.ResultPathReadMessages",
                comment="Read Messages from SQS",
                payload_response_only=True
                )

        ## STEP PROCESS MAP
        #Process Finish job
        lambda_process_finish_job = lbd.Function(
                    self, 'LambdaFunctionProcessFinishJob',
                    handler='lambda_function.lambda_handler',
                    code=lbd.Code.from_asset("lambda_sources/process_finish_job"),
                    runtime=lbd.Runtime.PYTHON_3_7,
                    timeout=cdk.Duration.seconds(300),
                    environment={
                        'QUEUE_URL_READY': queue_job_ready.queue_url,
                        'TABLE_NAME_JOBS': jobs_table.table_name
                    }

                )
        queue_job_ready.grant_consume_messages(lambda_process_finish_job)
        jobs_table.grant_read_write_data(lambda_process_finish_job)
        process_finish_job_task = sfnt.LambdaInvoke(
                self,
                "Process Finish Success Job",
                lambda_function=lambda_process_finish_job,
                payload=sfn.TaskInput.from_object({
                    "ReceiptHandle.$": "$.ReceiptHandle",
                    "JobId.$": "$.Body_json.id",
                    "Status": "SUCCESS",
                    "JobId.$": "$.Body_json.id",
                    }),
                comment="Process Finish Job",
                result_path="$.ProcessFinishJobResult",
                output_path="$.ProcessFinishJobResult.Description",
                payload_response_only=True
                )
        process_finish_job_task_failed = sfnt.LambdaInvoke(
                self,
                "Process Finish Failed Job",
                lambda_function=lambda_process_finish_job,
                payload=sfn.TaskInput.from_object({
                    "ReceiptHandle.$": "$.ReceiptHandle",
                    "JobId.$": "$.Body_json.id",
                    "Status": "FAILED"
                    }),
                comment="Process Finish Job",
                result_path="$.ProcessFinishJobFailedResult",
                output_path="$.ProcessFinishJobResult.Description",
                payload_response_only=True
                )

        #Process Start Job
        lambda_process_start_job = lbd.Function(
                    self, 'LambdaFunctionProcessStartJob',
                    handler='lambda_function.lambda_handler',
                    code=lbd.Code.from_asset("lambda_sources/process_start_job"),
                    runtime=lbd.Runtime.PYTHON_3_7,
                    timeout=cdk.Duration.seconds(300),
                    environment={
                        'TABLE_NAME_JOBS': jobs_table.table_name
                    }

                )
        jobs_table.grant_read_write_data(lambda_process_start_job)
        process_start_job_task = sfnt.LambdaInvoke(
                self,
                "Process Start Job",
                lambda_function=lambda_process_start_job,
                payload=sfn.TaskInput.from_object({
                    "ReceiptHandle.$": "$.ReceiptHandle",
                    "JobId.$": "$.Body_json.id"
                    }),
                comment="Process Start Job",
                result_path="$.ProcessStartJobResult",
                payload_response_only=True
            )
        # Define an AddStep Task for the Validation Step
        chain_step_process = _AddStepWithArgumentOverrides(
            self, 'StepProcessChain',
            emr_step=emr_code.EMRStep(
                name='Step Process Chain',
                jar='s3://{}.elasticmapreduce/libs/script-runner/script-runner.jar'.format(self.region),
                args=[
                    's3://{}/datamask/datamask-pyutil.sh'.format(artifacts_bucket.bucket_name),
                    's3://{}/datamask'.format(artifacts_bucket.bucket_name),
                    CONFIG_PATH,
                    'JOB_NAME',
                    'PART_LIST',
                ],
                #code=step_code
            ),
            fail_chain=process_finish_job_task_failed,
            cluster_id=sfn.TaskInput.from_json_path_at('$.ClusterId').value,
            result_path='$.ChainStepProcessResult',
            execution_input = sfn.TaskInput.from_json_path_at(f'$.Body_json').value,
            interval_retry = cdk.Duration.seconds(300),
            max_attempts_retry = 2 
        ) 

        process_start_job_task.next(chain_step_process)
        chain_step_process.next(process_finish_job_task)
        # Create a Parallel Task for the Phase 1 Steps
        step_process = sfn.Map(
                self, 
                'StepProcessMap', 
                #result_path='$',
                result_path='$.StepProcessMapResult',
                #output_path='$.ClusterId',
                items_path='$.ResultPathReadMessages.Payload').iterator(process_start_job_task)
        step_process.add_catch(terminate_failed_choice, errors=['States.ALL'], result_path='$.Error')

        ##SUCCESS CHAIN
        # A Chain for Success notification when the pipeline completes
        success = emr_chains.Success(
            self, 'SuccessChain',
            message=sfn.TaskInput.from_json_path_at('$'),
            subject='Pipeline Succeeded',
            topic=success_topic)

        # Define a Task to Terminate the Cluster
        terminate_successful_cluster = emr_tasks.TerminateClusterBuilder.build(
            self, 'TerminateSuccessfulCluster',
            name='Terminate Successful Cluster',
            cluster_id=sfn.TaskInput.from_json_path_at('$.ClusterId').value,
            result_path='$.TerminateSuccessfulClusterResult').add_catch(fail, errors=['States.ALL'], result_path='$.Error')
        # Desision to choice if launch the cluster or not
        terminate_successful_choice = sfn.Choice(
                    self, 
                    "Decision Terminate Success",
                    comment="Terminate on Success?"
                )
        terminate_successful_choice.when(sfn.Condition.string_equals("$.Launched","1"),terminate_successful_cluster.next(success)).otherwise(success)

        ##MAIN CHAIN
        # Set next for step_process
        read_messages_task.next(step_process).next(terminate_successful_choice)
        # Assemble the Pipeline

        definition = sfn.Chain\
                .start(check_messages_task)\
                .next(check_messages_choice.when(\
                        sfn.Condition.string_equals("$.CheckMessagesSQSResult.Payload.Flag","no"),\
                                success)\
                        .otherwise(\
                            launch_cluster_choice.when(\
                                sfn.Condition.string_equals("$.ClusterId",""),\
                                    launch_cluster\
                                    .next(pass_cluster_id_launched_to_read)
                                    .next(read_messages_task)
                                    )\
                                .otherwise(
                                    pass_cluster_id_execution_to_read\
                                    .next(read_messages_task)
                                    )\
                                )\
                    )


        ##STATE MACHINE        
        state_machine = sfn.StateMachine(
            self, 'TransientPipelineSQSTask',
            state_machine_name='datamask_pipeline', definition=definition)
        ######################################################################################
        ######################################################################################

        ## Process Event Lambda Function
        process_events = lbd.Function(
                    self, 'LambdaFunctionProcessEvent',
                    handler='lambda_function.lambda_handler',
                    code=lbd.Code.from_asset("lambda_sources/process_events"),
                    runtime=lbd.Runtime.PYTHON_3_7,
                    timeout=cdk.Duration.minutes(15),
                    memory_size=512,
                    environment={
                        'JOBS_TABLE': jobs_table.table_name,
                        'QUEUE_URL_READY':queue_job_ready.queue_url,
                        'QUEUE_URL_EVENTS':queue_s3_events.queue_url,
                        'TABLE_PREFIX_RE':TABLE_PREFIX_RE,
                        'FILE_EXCLUDE_RE': FILE_EXCLUDE_RE,
                        'FILE_INCLUDE_RE': FILE_INCLUDE_RE,
                        'CONFIG_PATH': CONFIG_PATH,
                        'STEP_FUNCTION_ARN': state_machine.state_machine_arn,
                        'CLUSTER_ID':''
                    }
                )

        jobs_table.grant_read_write_data(process_events)
        queue_s3_events.grant_consume_messages(process_events)
        queue_job_ready.grant_send_messages(process_events)
        artifacts_bucket.grant_read(process_events)
        state_machine.grant_start_execution(process_events)

        if CRON_WEEK_DAY != '*':
            process_events_scheduler = ev.Schedule.cron(week_day=CRON_WEEK_DAY,minute=CRON_MINUTE,hour=CRON_HOUR)
        else:
            process_events_scheduler = ev.Schedule.cron(day=CRON_DAY,minute=CRON_MINUTE,hour=CRON_HOUR)

        daily_rule = ev.Rule(
            self, "trigger_rule",
            schedule=process_events_scheduler)
        daily_rule.add_target(evt.LambdaFunction(process_events))