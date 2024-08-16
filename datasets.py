import json

import numpy as np
import pandas as pd

import db
from domain import types
import pickle

from rfl import get_rfl


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

    def is_string(column):
        return column_types['type'][column_types['column'].index(column)] == 'string'

    rfl = pd.DataFrame()
    for column in df.columns:
        df[column] = df[column].map(lambda x: try_float(x) if is_numeric(column) else x)
        if is_string(column):
            rfl[column] = get_rfl(df[column])

    rfl = pd.DataFrame(rfl.mode().iloc[0]).transpose().rename({0: 'FKGL_Category' })
    stats = df.describe(include='all')
    stats = pd.concat((stats, rfl))
    stats = stats.fillna(np.nan).replace([np.nan], [None])
    return stats.to_json()
