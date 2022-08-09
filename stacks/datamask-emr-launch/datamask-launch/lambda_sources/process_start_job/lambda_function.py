import json
import boto3
import os

sqs_client = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
table_name_jobs = os.environ['TABLE_NAME_JOBS']

def lambda_handler(event, context):

    table = dynamodb.Table(table_name_jobs)
    resp_update= table.update_item(
        Key={
            'id': event['JobId']
        },
        UpdateExpression="set JobStatus =:c",
        ExpressionAttributeValues={':c': 'EXECUTING'}
    )
    return {"Payload": resp_update, "Description": "Job Start was processed"}
