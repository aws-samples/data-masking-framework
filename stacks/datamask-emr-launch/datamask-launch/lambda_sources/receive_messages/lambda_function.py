import json
import boto3
import os


queue_url = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    sqs_client = boto3.client('sqs')
    #print("start function")
    messages = []
    resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=2,
            VisibilityTimeout=60
        )   
    #print("Start while")    
    cc = 0
    while 'Messages' in resp:
        for m in resp['Messages']:
            cc = cc + 1
            if 'Tag' in event and 'Value' in event:
                m[event['Tag']]=event['Value']
            message = {}    
            message["Body_json"]=json.loads(m["Body"])
            message["ReceiptHandle"] = m["ReceiptHandle"]
            message["ClusterId"] = m["ClusterId"]
            messages.append(message) 
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=2, 
            VisibilityTimeout=60
        )

    #print("messages end:",messages)
    if len(messages) == 0:
        return { "Payload": messages, "Description": "No messages"}
    else:
        return { "Payload": messages, "Description": "Trere are {} messages".format(cc)}

