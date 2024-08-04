import pandas as pd
import numpy as np

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


def outliers(df):
    # Function to convert columns to the appropriate data type
    data_frame = convert_column_types(df.copy())

    def detect_outliers_std(data_frame, column):
        mean = data_frame[column].mean()
        std = data_frame[column].std()
        threshold = 3  # Typically 3 standard deviations
        outliers = data_frame[
            (data_frame[column] > mean + threshold * std) | (data_frame[column] < mean - threshold * std)]
        return outliers

    # Loop through each column in the dataframe
    outlier_percentages = {}  # Initialize a dictionary to store outlier percentages
    for column in data_frame.columns:
        if data_frame[column].dtype in [np.float64, np.int64]:
            # print(f"\nColumn: {column}")

            # Detect outliers using Standard Deviation Method
            outliers_std = detect_outliers_std(data_frame, column)

            outlier_percentage = len(outliers_std) / len(data_frame) * 100
            outlier_percentages[column] = outlier_percentage

        else:
            # print(f"\nSkipping column {column} as it is not numerical.")
            outlier_percentages[column] = 'Not Numeric'  # Mark non-numerical columns
    return outlier_percentages
