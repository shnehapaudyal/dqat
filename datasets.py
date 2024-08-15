import numpy as np

import db
from domain import types


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

    for column in df.columns:
        df[column] = df[column].map(
            lambda x: try_float(x) if column_types['type'][column_types['column'].index(column)] in ['float',
                                                                                                     'integer'] else x)

    return df.describe(include='all').to_json()
