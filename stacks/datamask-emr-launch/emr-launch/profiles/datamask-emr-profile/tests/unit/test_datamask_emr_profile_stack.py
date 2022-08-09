import json
import pytest

from aws_cdk import core
from datamask-emr-profile.datamask_emr_profile_stack import DatamaskEmrProfileStack


def get_template():
    app = core.App()
    DatamaskEmrProfileStack(app, "datamask-emr-profile")
    return json.dumps(app.synth().get_stack("datamask-emr-profile").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
