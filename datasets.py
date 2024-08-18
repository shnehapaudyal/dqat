import json

import numpy as np
import pandas as pd

import db
from domain import types
import pickle

def get_dataset(dataset_id):
    return db.read_dataset(dataset_id)


def get_datatypes(df):
    return types.get_type_info(df)[1]


def statistics(df):
    column_types = get_datatypes(df).to_dict(orient='list')

    def try_float(value):
        try:
            return float(value)
        except ValueError:
            return np.nan

    def is_numeric(column):
        return column_types['type'][column_types['column'].index(column)] in ['float', 'integer']

    stats = df.describe(include='all')

    for column in df.columns:
        df[column] = df[column].map(lambda x: try_float(x) if is_numeric(column) else x)

    stats = stats.fillna(np.nan).replace([np.nan], [None])
    return stats.to_json()



try:
    with open('model/classifier.pkl', 'rb') as file:
        tags_classifier = pickle.load(file)
except Exception as e:
    print('Error', e)


def get_tags(df):
    return list(tags_classifier.predict(df.columns))
