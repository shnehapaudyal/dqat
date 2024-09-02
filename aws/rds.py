# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import json
import os
import urllib.parse

import boto3

from aws.secretmanager import get_secret

aws_secret_key = os.environ['RDS_SECRET_KEY']
rds_host = os.environ['RDS_HOST']


def get_rds_secret():
    secret = get_secret(aws_secret_key)
    return json.loads(secret)


def get_config():
    static_config = {"host": rds_host, "port": '5432',
                     "database": "dataset_records"}

    credentials = get_rds_secret()
    static_config["username"] = credentials["username"]
    static_config["password"] = urllib.parse.quote(credentials["password"])

    return static_config


if __name__ == '__main__':
    print(get_rds_secret())
