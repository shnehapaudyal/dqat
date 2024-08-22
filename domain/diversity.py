import pandas as pd
from domain import types
from domain.readability import preprocess_text


def calculate_diversity(df, type_info):
    data_types, column_types, _ = type_info

    string_columns = column_types[(column_types['type'] == 'string')]['column'].values

    if len(string_columns) == 0:
        return None

    def pre_process(value):
        return preprocess_text(str(value))

    column_diversity = 0
    explode = df[string_columns].map(pre_process).map(lambda x: x.split()).apply(pd.Series.explode)
    column_diversity += explode.drop_duplicates().size / explode.size

    diversity = column_diversity / len(string_columns)
    return diversity * 100
