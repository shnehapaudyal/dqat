import os

from server import app


def save(file, filename):
    # Initialize a boto3 client for S3
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)  # Then save the file
    return os.stat(file_path).st_size, file_path


def delete(file_path):
    os.remove(file_path)