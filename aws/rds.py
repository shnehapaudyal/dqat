# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/
import json
import urllib.parse

import boto3

from aws.secretmanager import get_secret


def get_rds_secret():
    secret = get_secret('rds!db-cf5a6190-9efd-42c9-a314-dce6cbdd509b')
    return json.loads(secret)


def get_config():
    static_config = {"host": "dqaat-database-1.czkcmkceefx5.eu-west-1.rds.amazonaws.com", "port": '5432',
                     "database": "dataset_records"}

    credentials = get_rds_secret()
    static_config["username"] = credentials["username"]
    static_config["password"] = urllib.parse.quote(credentials["password"])

    return static_config


if __name__ == '__main__':
    print(get_rds_secret())
