# Sample DataFrame
import json
import re
from collections import Counter

import uuid

import pandas as pd

# Extended patterns for dates, times, and datetimes
date_patterns = [
    r'^\d{4}[-/]\d{2}[-/]\d{2}$',  # YYYY-MM-DD or YYYY/MM/DD
    r'^\d{2}[-/]\d{2}[-/]\d{4}$',  # MM-DD-YYYY or DD-MM-YYYY
    r'^\d{2}[-/]\d{2}[-/]\d{2}$',  # MM-DD-YY or DD-MM-YY
    r'^\d{1,2}-[A-Za-z]{3}-\d{4}$'  # DD-MMM-YYYY (e.g., 10-Aug-2023)
]

time_patterns = [
    r'^\d{2}:\d{2}(:\d{2})?$',  # HH:MM or HH:MM:SS
    r'^\d{1,2}:\d{2}\s?[APap][Mm]$',  # HH:MM AM/PM (e.g., 3:30 PM)
    r'^\d{2}:\d{2}:\d{2}\.\d{3}$',  # HH:MM:SS.sss (e.g., 15:30:45.123)
    r'^\d{1,2}:\d{2}:\d{2}$'  # H:MM:SS (e.g., 3:30:15)
]

datetime_patterns = [
    r'^\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}(:\d{2})?$',  # YYYY-MM-DD HH:MM:SS or YYYY/MM/DD HH:MM
    r'^\d{2}[-/]\d{2}[-/]\d{4}[ T]\d{2}:\d{2}$',  # MM-DD-YYYY HH:MM or DD-MM-YYYY HH:MM
    r'^\d{1,2}-[A-Za-z]{3}-\d{4}\s+\d{2}:\d{2}:\d{2}$',  # DD-MMM-YYYY HH:MM:SS (e.g., 10-Aug-2023 03:30:15)
    r'^[A-Za-z]{3}\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s?[APap][Mm]$'
    # MMM DD, YYYY HH:MM AM/PM (e.g., Aug 10, 2023 3:30 PM)
]


# Function to classify the type of each value
def classify_value(value):
    try:
        cleaned_value = str(value).replace(',', '')

        # Check for integer
        if re.match(r'^-?\d+$', cleaned_value):
            return 'integer'

        # Check for float
        if re.match(r'^-?\d*\.\d+$|^-?\d+(\.\d+)?[eE][-+]?\d+$', cleaned_value):
            return 'float'

        # Check for UUID
        try:
            uuid_obj = uuid.UUID(value, version=4)
            return 'uuid'
        except ValueError:
            pass

        # Check for JSON
        try:
            json_obj = json.loads(value)
            return 'json'
        except ValueError:
            pass

        # Check for datetime
        for pattern in datetime_patterns:
            if re.match(pattern, value):
                return 'datetime'

        # Check for date
        for pattern in date_patterns:
            if re.match(pattern, value):
                return 'date'

        # Check for time
        for pattern in time_patterns:
            if re.match(pattern, value):
                return 'time'

        # If no matches, consider it a string
        return 'string'
    except Exception as e:
        return 'unknown'


# Function to detect and reclassify enums in a column
def detect_and_reclassify_enums(column_data):
    initial_classified_types = column_data.apply(classify_value)

    # Identify potential enums
    string_values = column_data[initial_classified_types == 'string']
    value_counts = Counter(string_values)
    potential_enums = [key for key, count in value_counts.items() if count > 1]

    # Reclassify as enums
    def reclassify(value):
        if value in potential_enums:
            return 'enum'
        return classify_value(value)

    return column_data.apply(reclassify)


def aggregate_column_types(classified_df):
    # Create an empty list to store the column information
    column_info = []

    # Iterate over each column in the DataFrame
    for column in classified_df.columns:
        # Get the value counts for the column
        value_counts = classified_df[column].value_counts()
        # Get the most frequent value
        most_frequent_value = value_counts.index[0]
        # Append the column name, most frequent value, and its type to the list

        column_info.append((column, most_frequent_value))

    # Create a new DataFrame from the column information
    return column_info


def get_column_types(df):
    classified_df = df.apply(detect_and_reclassify_enums)
    return aggregate_column_types(classified_df)
