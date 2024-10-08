import re
from datetime import datetime

import pandas as pd
import numpy as np
from pandas import Series
from sklearn.preprocessing import StandardScaler

import domain.types
from domain.consistency import is_numeric


# def is_numeric(value):  # Converting the datatypes according to the dataset values
#     try:
#         float(value)
#         return True
#     except ValueError:
#         return False


def clean_and_convert_column(column):
    """Remove commas from values and convert columns based on their content."""
    if column.dtype == 'object':
        # Remove commas from column values
        cleaned_column = column.str.replace(',', '', regex=False)

        # Determine if the column is numeric or text
        numeric_count = cleaned_column.apply(is_numeric).sum()
        total_count = len(cleaned_column)
        string_count = total_count - numeric_count

        # If the majority of values are numeric, convert to numeric
        if numeric_count > string_count:
            # Convert to numeric and handle NaN
            numeric_column = pd.to_numeric(cleaned_column, errors='coerce')
            # Check if all non-NaN values are integers
            if numeric_column.dropna().apply(lambda x: x % 1 == 0).all():
                # loop through each items in numeric_column, convert to NA if not valid integer
                converted = cleaned_column.apply(lambda x: np.nan if not is_numeric(x, int) else x)
            else:
                converted = numeric_column.apply(lambda x: np.nan if not is_numeric(x) else x)
        else:
            converted = column.apply(lambda x: None if is_numeric(x) else x)
        return converted
    else:
        # If the column is not of type object, return it as is
        return column


def convert_column_types(df):
    """Apply conversion to all columns in the DataFrame."""
    for column in df.columns:
        df[column] = clean_and_convert_column(df[column])
    return df


def detect_outliers(df, column):
    z_scores = StandardScaler().fit_transform(df[[column]])
    z_scores = np.power(z_scores, 2)
    return (z_scores > 9).sum() / df[column].size * 100

    # def detect_outliers_std(column: Series):
    #     mean = column.mean()
    #     std = column.std()
    #     threshold = 3  # Typically 3 standard deviations
    #     try:
    #         return (column > mean + threshold * std) | (column < mean - threshold * std)
    #     except Exception as e:
    #         print(f"Error occurred while detecting outliers: {e}")
    #         return column.apply(lambda x: False)
    #
    # outliers_std = detect_outliers_std(column).sum()
    # outlier_percentage = outliers_std / len(column) * 100
    # return outlier_percentage


def detect_numeric_outliers(df, column):
    def clean_value(value):
        return value if isinstance(value, (int, float)) else value.replace(',', '') if value is not None else ''

    df[f'{column}_numeric'] = pd.to_numeric(df[column].map(clean_value), errors='coerce')
    outliers = detect_outliers(df, f'{column}_numeric')

    df.drop(columns=[f'{column}_numeric'], inplace=True)  # Drop the temporary numeric column

    return outliers


def detect_datetime_outliers(df, column):
    supported_formats = []
    supported_formats.extend(domain.types.date_patterns)
    supported_formats.extend(domain.types.time_patterns)
    supported_formats.extend(domain.types.datetime_patterns)

    df[f'{column}_timestamp'] = pd.to_datetime(df[column], errors='coerce').map(
        lambda x: 0 if pd.isnull(x) else x.timestamp())

    def map_datetime(value):
        if not value:
            return 0

        for pattern in domain.types.datetime_patterns:
            try:
                if re.match(pattern, str(value)):
                    dt = datetime.strptime(value, pattern)
                    return dt.timestamp()
            except ValueError as e:
                continue
        return 0

    # df[f'{column}_timestamp'] = df[column].map(map_datetime)
    outliers = detect_outliers(df, f'{column}_timestamp')

    df.drop(columns=[f'{column}_timestamp'], inplace=True)  # Drop the temporary timestamp column

    return outliers


def detect_string_outliers(df, column):
    df[f'{column}_len'] = df[column].apply(lambda x: 0 if pd.isnull(x) else len(str(x)))
    outliers = detect_outliers(df, f'{column}_len')
    df.drop(columns=[f'{column}_len'], inplace=True)  # Drop the temporary length column
    return outliers


def detect_enum_outliers(df, column):
    freq = df[column].value_counts()
    df[f'{column}_frequency'] = df[column].apply(lambda x: 0 if pd.isnull(x) else freq[x])

    outlier = detect_outliers(df, f'{column}_frequency')
    df.drop(columns=[f'{column}_frequency'], inplace=True)  # Drop the temporary length column

    return outlier


def outliers(df, type_info):
    # Function to convert columns to the appropriate data type

    column_types: pd.DataFrame = type_info[1]
    numeric_columns = column_types[(column_types['type'] == 'integer') | (column_types['type'] == 'float')][
        'column'].values
    datetime_columns = column_types[
        (column_types['type'] == 'date') | (column_types['type'] == 'time') | (column_types['type'] == 'datetime')][
        'column'].values
    string_columns = column_types[(column_types['type'] == 'string')][
        'column'].values
    enum_columns = column_types[(column_types['type'] == 'enum')][
        'column'].values

    # Loop through each column in the dataframe
    outlier_percentages = {}  # Initialize a dictionary to store outlier percentages
    for column in df.columns:
        if column in numeric_columns:
            outlier_percentages[column] = detect_numeric_outliers(df, column)
        elif column in datetime_columns:
            outlier_percentages[column] = detect_datetime_outliers(df, column)
        elif column in string_columns:
            outlier_percentages[column] = detect_string_outliers(df, column)
        elif column in enum_columns:
            outlier_percentages[column] = detect_enum_outliers(df, column)
        else:
            outlier_percentages[column] = 0

    return outlier_percentages
