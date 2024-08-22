import pandas as pd
from domain import types


def calculate_diversity(df, type_info):
    data_types, column_types, _ = type_info

    columns = column_types[column_types['type'] == 'string']['column'].values

    if len(columns) == 0:
        return None

    def calculate_ttr(value):
        unique_words = set(value.split())
        ttr = len(unique_words) / (len(value))
        return ttr

    string_columns = column_types[(column_types['type'] == 'string')]['column'].values

    # diversity = 0
    column_diversity = 0
    for column in df.columns:
        if column in string_columns:
            explode = df[column].map(lambda x: str(x).split()).explode(column)
            column_diversity += len(set(explode)) / len(explode)
        else:
            column_diversity += 1

    diversity = column_diversity / len(df.columns)
    return diversity * 100