import pandas as pd
from domain import types


def calculate_diversity(df, type_info):
    data_types, column_types, _ = type_info

    columns = column_types[column_types['type'] == 'string']['column']
    if len(columns) == 0:
        return 100

    def calculate_ttr(column):
        unique_words = set(column.split())
        ttr = len(unique_words) / (len(column))
        return ttr

    # diversity = 0
    column_diversity = df[columns].map(calculate_ttr)
    diversity = column_diversity.mean().mean()
    return diversity * 100