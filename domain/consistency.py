import pandas as pd
import numpy as np
from domain import types


# Sample DataFrame
def sample_dataframe():
    data = {
        'A': ['1,000', '2,000', '30,000', '45,000'],  # Numeric with commas
        'B': ['25,000', '32,000', '4,000', '20.2'],  # Numeric with commas
        'C': ["this is text, can you check?", '20', "Hi, there!", "this is it"],  # Text
        'D': ['twenty', '20', '45', '10'],
        'E': ['2022/01/05', '2022/02/10', '2022/03/15', '2022/04/20'],
        'F': ['50.0085', '20.02', '45.001', 'Forty'],  # Mixed content
        # Mixed content
    }
    return pd.DataFrame(data)


def is_numeric(value, number_type=float):
    """Check if a value is numeric (after removing commas)."""
    try:
        number_type(value)
        return True
    except ValueError:
        return False


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


def calculate_consistency(df, type_info):
    total_values = df.size

    data_types, column_types, consistency_values = type_info

    # Count the number of False values in consistency_values
    consistent_values = consistency_values.sum().sum()

    df_consistency = (consistent_values / total_values) * 100
    return df_consistency


def inconsistency(df, type_info):
    data_types, column_types, consistency_values = type_info

    # Count the number of False values in consistency_values
    consistent_values = consistency_values.sum()

    df_consistency = {}
    for column in df.columns:
        total_values = df[column].size
        df_consistency[column] = (1 - consistent_values[column] / total_values) * 100

    return df_consistency


if __name__ == '__main__':
    dataframe = sample_dataframe()
    print(calculate_consistency(dataframe, types.get_column_types(dataframe)))
