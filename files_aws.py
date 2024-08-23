import threading

import boto3
import pandas as pd
import files_local
from server import app
from functools import lru_cache

bucket_name = app.config['UPLOAD_BUCKET']


def save(file, filename):
    # Initialize a boto3 client for S3
    s3 = boto3.client('s3')

    size, path = files_local.save(file, filename)

    # Upload the file to the specified S3 bucket and key
    response = s3.upload_file(path, bucket_name, filename)

    files_local.delete(path)
    print(response, size, filename)

    return size, filename


files_cache = {}
read_lock = threading.Lock()


def read(filename):
    # Create a lock object
    with read_lock:
        if filename in files_cache:
            return files_cache[filename]
        bucket_file = f"s3://{bucket_name}/{filename}"
        print(bucket_file)
        df = pd.read_csv(bucket_file)
        files_cache[filename] = df
        return df
