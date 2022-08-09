import json
import boto3
import os
import time

sqs_client = boto3.client('sqs')


def lambda_handler(event, context):
    queue_url = os.environ['QUEUE_URL']
    #print("start function")
    messages = []
    payload = {}
    resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            WaitTimeSeconds=2,
            VisibilityTimeout=1
        )
    #print(resp)
    if 'Messages' in resp:
        for m in resp['Messages']:
            messages.append(m)
    payload["Payload"]={}
    #print("messages end:",messages)
    if len(messages) == 0:
        payload["Payload"]["Flag"] = "no"
        payload["Description"] = "There are not any messages"
    else:
        payload["Payload"]["Flag"] = "yes"
        payload["Description"] = "There are messages"
    time.sleep(5)
    return payload
