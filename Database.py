import pandas as pd
import uuid
from datetime import datetime
import json
import re
import psycopg2
from psycopg2.extras import Json


def assess_dataset(file_path):
    df = pd.read_csv(file_path)

    dataset_id = str(uuid.uuid4())
    created_timestamp = datetime.now().isoformat()

    formats = {"date": r"\d{4}-\d{2}-\d{2}",
               "time": r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
               "email": r"[^@]+@[^@]+\.[^@]+",
               "zip_code": r"\b\d{5}\b",
               "credit_card": r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
               "url": r"https?://[^\s]+",
               "uk_postal_code": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
               "canadian_postal_code": r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$"
               }

    detected_formats = {}
    for column in df.columns:
        column_formats = []
        for format_name, regex_list in formats.items():
            for regex in regex_list:
                if df[column].astype(str).str.match(regex).any():
                    column_formats.append(format_name)
        if column_formats:
            detected_formats[column] = column_formats[0]

    dtypes = df.dtypes.apply(lambda x: x.name).to_dict()

    dataset = {
        'id': dataset_id,
        'filename': file_path.split("/")[-1],
        'created': created_timestamp,
        'formats': detected_formats,
        'dtypes': dtypes
    }

    return dataset


def insert_dataset(dataset, db_config):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    insert_query = """
    INSERT INTO datasets (id, filename, created, formats, dtypes)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(insert_query, (
        dataset['id'],
        dataset['filename'],
        dataset['created'],
        Json(dataset['formats']),
        Json(dataset['dtypes'])
    ))

    conn.commit()
    cur.close()
    conn.close()


file_path = 'path/to/your/file.csv'
dataset = assess_dataset(file_path)

db_config = {
    'dbname': 'your_database',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

insert_dataset(dataset, db_config)