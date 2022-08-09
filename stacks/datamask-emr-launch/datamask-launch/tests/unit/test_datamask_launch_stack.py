import json
import pytest

from aws_cdk import core
from datamask-launch.datamask_launch_stack import DatamaskLaunchStack


def get_template():
    app = core.App()
    DatamaskLaunchStack(app, "datamask-launch")
    return json.dumps(app.synth().get_stack("datamask-launch").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
