import re

import pandas as pd


def convert_matching_format(value, formats):
    if not value:
        return -1
    try:
        for format in formats:
            if re.match(format, str(value)):
                return formats.index(format), str(format)
    except Exception as e:
        print(f"Error occurred while converting value to format: {e}")
    return -1


def calculate_conformity(df, formats, type_info):
    total_values = df.size
    conforming_values = 0

    column_types = type_info[1]
    numeric_columns = column_types[(column_types['type'] == 'integer') | (column_types['type'] == 'float')][
        'column'].values

    cleaned_df = pd.DataFrame()
    for column in df.columns:
        cleaned_df[column] = df[column].map(
            lambda x: x if column not in numeric_columns else str(x).replace(',', ''))

    df_conformity = cleaned_df.map(lambda x: convert_matching_format(x, formats))
    mode_values = df_conformity.mode().iloc[0]

    data_types, column_types, consistency_values = type_info

    value_conformity = df_conformity == mode_values
    type_conformity = data_types == data_types.mode().iloc[0]
    conforming_values = value_conformity & type_conformity

    conformity = (conforming_values.sum().sum() / total_values) * 100
    return conformity


def match_supported_format(value, supported_formats):
    for format in supported_formats:
        if re.match(format, str(value)):
            return supported_formats.index(format)
    return -1


def create_matching_dataframe(df, supported_formats):
    matching_df = df.copy()
    for column in df.columns:
        matching_df[column] = df[column].apply(lambda x: match_supported_format(x, supported_formats))
    return matching_df


def find_max_occurrences(df):
    max_occurrences_list = {}

    for column in df.columns:
        value_counts = df[column].value_counts()
        if not value_counts.empty:
            max_occurrences = value_counts.idxmax()
            max_occurrences_list[column] = max_occurrences

    return max_occurrences_list


def inconsistent_format(df):
    supported_formats = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{2}-\d{2}-\d{4}",
        r"\d{1,2}/\d{1,2}/\d{4}",
        r"\d{1}/\d{2}/\d{4}",
        r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
        r"[^@]+@[^@]+\.[^@]+",
        r"\b\d{5}\b",
        r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
        r"https?://[^\s]+",
        r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
        r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$",
        # r".*"
    ]

    format_specification_df = create_matching_dataframe(df, supported_formats)
    dataframe_formats = find_max_occurrences(format_specification_df)

    print(format_specification_df)

    result = {'data': format_specification_df.to_dict(), 'value': {}}
    for column in format_specification_df.columns:
        column_specs = dataframe_formats[column]
        items = format_specification_df[column].value_counts()[column_specs]
        result['value'][column] = (1 - items / len(format_specification_df[column])) * 100

    return result


def invalid_formats(df, formats, type_info):
    column_types = type_info[1]

    numeric_columns = column_types[(column_types['type'] == 'integer') | (column_types['type'] == 'float')][
        'column'].values

    cleaned_df = pd.DataFrame()
    for column in df.columns:
        cleaned_df[column] = df[column].map(
            lambda x: x if column not in numeric_columns else str(x).replace(',', ''))
    df_conformity = cleaned_df.map(lambda x: convert_matching_format(x, formats))
    mode_values = df_conformity.mode().iloc[0]

    data_types = type_info[0]

    value_conformity = df_conformity == mode_values
    type_conformity = data_types == data_types.mode().iloc[0]
    conforming_values = value_conformity & type_conformity

    conformity = {}
    for column in df.columns:
        total_values = df[column].size
        conformity[column] = (1 - conforming_values[column].sum() / total_values) * 100

    return conformity
