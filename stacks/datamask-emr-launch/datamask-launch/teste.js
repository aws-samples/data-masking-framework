import * as cr from '@aws-cdk/custom-resources';
import * as logs from '@aws-cdk/aws-logs';
import * as s3 from '@aws-cdk/aws-s3';
import * as sqs from '@aws-cdk/aws-sqs';
import * as iam from '@aws-cdk/aws-iam';
import {Construct} from '@aws-cdk/core';

// You can drop this construct anywhere, and in your stack, invoke it like this:
// const s3ToSQSNotification = new S3NotificationToSQSCustomResource(this, 's3ToSQSNotification', existingBucket, queue);

export class S3NotificationToSQSCustomResource extends Construct {

    constructor(scope: Construct, id: string, bucket: s3.IBucket, queue: sqs.Queue) {
        super(scope, id);

        // https://stackoverflow.com/questions/58087772/aws-cdk-how-to-add-an-event-notification-to-an-existing-s3-bucket
        const notificationResource = new cr.AwsCustomResource(scope, id+"CustomResource", {
            onCreate: {
                service: 'S3',
                action: 'putBucketNotificationConfiguration',
                parameters: {
                    // This bucket must be in the same region you are deploying to
                    Bucket: bucket.bucketName,
                    NotificationConfiguration: {
                        QueueConfigurations: [
                            {
                                Events: ['s3:ObjectCreated:*'],
                                QueueArn: queue.queueArn,
                            }
                        ]
                    }
                },
                physicalResourceId: <cr.PhysicalResourceId>(id + Date.now().toString()),
            },
            onDelete: {
                service: 'S3',
                action: 'putBucketNotificationConfiguration',
                parameters: {
                    // This bucket must be in the same region you are deploying to
                    Bucket: bucket.bucketName,
                    // deleting a notification configuration involves setting it to empty.
                    NotificationConfiguration: {
                    }
                },
                physicalResourceId: <cr.PhysicalResourceId>(id + Date.now().toString()),
            },
            policy: cr.AwsCustomResourcePolicy.fromStatements([new iam.PolicyStatement({
                // The actual function is PutBucketNotificationConfiguration.
                // The "Action" for IAM policies is PutBucketNotification.
                // https://docs.aws.amazon.com/AmazonS3/latest/dev/list_amazons3.html#amazons3-actions-as-permissions
                actions: ["S3:PutBucketNotification"],
                 // allow this custom resource to modify this bucket
                resources: [bucket.bucketArn],
            })]),
            logRetention: logs.RetentionDays.ONE_DAY,
        });

        // allow S3 to send notifications to our queue
        // https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#grant-destinations-permissions-to-s3
        queue.addToResourcePolicy(new iam.PolicyStatement({
            principals: [new iam.ServicePrincipal("s3.amazonaws.com")],
            actions: ["SQS:SendMessage"],
            resources: [queue.queueArn],
            conditions: {
                ArnEquals: {"aws:SourceArn": bucket.bucketArn}
            }
        }));

        // don't create the notification custom-resource until after both the bucket and queue
        // are fully created and policies applied.
        notificationResource.node.addDependency(bucket);
        notificationResource.node.addDependency(queue);
    }
