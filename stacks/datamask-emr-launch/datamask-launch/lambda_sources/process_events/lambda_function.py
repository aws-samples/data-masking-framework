import json
import boto3
from botocore.errorfactory import ClientError
import os
import uuid
import re
from datetime import datetime
from time import sleep

sqs_client = boto3.client('sqs')
s3 = boto3.client('s3')
sf = boto3.client('stepfunctions')
dynamodb = boto3.resource('dynamodb')
jobs_table = os.environ['JOBS_TABLE']
queue_url_ready = os.environ['QUEUE_URL_READY']
queue_url_events = os.environ['QUEUE_URL_EVENTS']
table_prefix_re = os.environ['TABLE_PREFIX_RE']
file_exclude_re = os.environ['FILE_EXCLUDE_RE']
file_include_re = os.environ['FILE_INCLUDE_RE']
config_path = os.environ['CONFIG_PATH']
step_function_arn = os.environ['STEP_FUNCTION_ARN']
cluster_id = os.environ['CLUSTER_ID']

def load_config(config_path):
    config_split = config_path.split("/")
    bucket = config_split[2]
    key = ""
    first = True
    for token in config_split[3:]:
        if first:
            key = token
            first = False
        else:
            key = "{}/{}".format(key,token)
    print("bucket: {}".format(bucket))
    print("key: {}".format(key))
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        return json.loads(resp['Body'].read().decode('utf-8'))
    except ClientError:
        return None


def lambda_handler(event, context):
    
    config_dict = load_config(config_path)
        
    if not config_dict:
        print("Can not read config file")
        return None

    if 'Jobs' not in config_dict:
        print("Can not find Jobs key in the config file")
        return None

    input_path = {}    
    for job in config_dict['Jobs']:
        if 'Input' not in job or 'InputPath' not in job['Input']:
            print("Can not find InputPath key in the config file for Job {}".format(job))
        else:
            input_path[job['Input']['InputPath']]=job['JobName']      

    #print("start function")
    resp = sqs_client.receive_message(
            QueueUrl=queue_url_events,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            VisibilityTimeout=900
        )
    #print("Start while")    
    #Get all messages
    map_table = {}
    events = {}
    while 'Messages' in resp:
        for m in resp['Messages']:
            m_json = json.loads(m["Body"])
            for rec in m_json:
                if "Records" in rec:
                    for rec2 in m_json["Records"]:
                        if rec2["s3"]["object"]["size"] > 0 \
                        and not re.search(file_exclude_re, rec2["s3"]["object"]["key"]) \
                        and re.search(file_include_re, rec2["s3"]["object"]["key"]):
                            bucket_name = rec2["s3"]["bucket"]["name"]
                            key=rec2["s3"]["object"]["key"].replace('%3D','=')
                            table_prefix_match = re.search(table_prefix_re,key)
                            table_prefix = table_prefix_match.group()
                            partition = ''
                            for p in key[table_prefix_match.end():].split("/")[:-1]:
                                if partition == '':
                                    partition = p
                                else:
                                    partition = '{}/{}'.format(partition,p)
                            table_path = "s3://{}/{}".format(bucket_name,table_prefix)

                            if table_path in input_path:
                                if table_prefix not in map_table:
                                    map_table[table_prefix]={}
                                    events[table_prefix]={}
                                    map_table[table_prefix]["JobName"]=input_path[table_path]
                                    map_table[table_prefix]["TablePath"]=table_path
                                    map_table[table_prefix]["CreatedTimestamp"]=datetime.now().isoformat()
                                    parameter_radical=table_prefix.replace("/","_")
                                    map_table[table_prefix]['JobStatus'] = 'WAITING'
                                    map_table[table_prefix]["StepArgumentOverrides"]={
                                        "Step Process Chain": {
                                            "PART_LIST": partition,
                                            "JOB_NAME": input_path[table_path],
                                        }
                                    }
                                    events[table_prefix]["Events"]=[]
                                    events[table_prefix]["Events"].append(m)
                                else:    
                                    events[table_prefix]["Events"].append(m)
                                    if  map_table[table_prefix]["StepArgumentOverrides"]["Step Process Chain"]["PART_LIST"].find(partition) == -1:
                                        map_table[table_prefix]["StepArgumentOverrides"]["Step Process Chain"]["PART_LIST"] = \
                                            "{},{}".format(
                                                    map_table[table_prefix]["StepArgumentOverrides"]["Step Process Chain"]["PART_LIST"],
                                                    partition
                                                    )
                            else:
                                print('Table path {} is not in config'.format(table_path))

        resp = sqs_client.receive_message(
            QueueUrl=queue_url_events,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            VisibilityTimeout=60
        )
    jobs=[]
    for tab in map_table:

        table = dynamodb.Table(jobs_table)
        map_table[tab]['id'] = map_table[tab]['JobName']
        response = table.put_item(Item=map_table[tab])
        if map_table[tab]['JobStatus'] == 'WAITING':
            resp = sqs_client.send_message(
                QueueUrl=queue_url_ready,
                MessageBody=json.dumps(map_table[tab]))
            if resp["ResponseMetadata"]['HTTPStatusCode'] != 200:
                print('Failed to send job {} to job ready queue '.format(map_table[tab]['JobId']))
            else:
                for message in events[tab]["Events"]:
                    resp2 = sqs_client.delete_message(
                        QueueUrl=queue_url_events, 
                        ReceiptHandle=message["ReceiptHandle"]
                        )
                    if resp2["ResponseMetadata"]['HTTPStatusCode'] != 200:
                        print('Failed to delete message from  queue {}'.format(message["ReceiptHandle"]))
    sf_input = { 'ClusterId': cluster_id }
    
    response = sf.start_execution(
        stateMachineArn=step_function_arn,
        name='DatamaskPipeline-{}'.format(str(uuid.uuid1())),
        input=json.dumps(sf_input)
    )
    
    return map_table





