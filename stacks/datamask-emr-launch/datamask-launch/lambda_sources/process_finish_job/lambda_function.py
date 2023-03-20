import json
import boto3
import os

sqs_client = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
queue_url_ready = os.environ['QUEUE_URL_READY']
table_name_jobs = os.environ['TABLE_NAME_JOBS']

def lambda_handler(event, context):

    table = dynamodb.Table(table_name_jobs)
    resp_update= table.update_item(
        Key={
            'id': event['JobId']
        },
        UpdateExpression="set JobStatus=:c",
        ExpressionAttributeValues={':c': event['Status']}
    )
    resp = ''
    description = ''
    if event['Status'] == 'SUCCESS':
        resp = sqs_client.delete_message(
            QueueUrl=queue_url_ready, ReceiptHandle=event["ReceiptHandle"]
        )
        if resp["ResponseMetadata"]['HTTPStatusCode'] != 200:
            description = "Failed to delete message"
        else:
            description = "Job Finish was processed"
    else:
        description = 'Status not Success'

    payload = {
                "RespUpdateJobs": resp_update,
                "RespDeleteMessage": resp
    }

    ret = {"Payload": payload, "Description": description}
    print(ret)
    print(event['Status'])
    if event['Status'] == 'SUCCESS': 
        return ret
    else:
        raise ValueError(ret)



