import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from domain.readability import preprocess_text
from domain.types import get_timestamp_value


def calculate_ease_of_manipulation(df, type_info):
    # Align the DataFrames to ensure they have identical indices and columns
    try:
        cleaned_df = clean_df(df, type_info)
        df, cleaned_df = df.align(cleaned_df, join='outer', fill_value=float('nan'))
        differences = (df != cleaned_df).sum().sum()
        total_values = df.size
        ease_of_manipulation = (1 - differences / total_values) * 100
        return ease_of_manipulation
    except Exception as e:
        print(f"Error occurred while cleaning DataFrame: {e}")
        raise e


def clean_df(df, type_info):
    df = df.copy()
    data_types, column_types, consistency_values = type_info

    string_columns = column_types[column_types['type'] == 'string']['column'].values
    enum_columns = column_types[column_types['type'] == 'enum']['column'].values
    numeric_columns = pd.concat((
        column_types[column_types['type'] == 'integer']['column'],
        column_types[column_types['type'] == 'float']['column']
    )).values
    datetime_columns = column_types[column_types['type'] == 'datetime']['column'].values

    df[numeric_columns] = df[numeric_columns].map(lambda x: x if x is None else str(x).replace(',', ''))
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    if len(numeric_columns) > 0:
        df[numeric_columns] = SimpleImputer(strategy='median').fit_transform(df[numeric_columns])
    if len(enum_columns) > 0:
        df[enum_columns] = SimpleImputer(strategy='most_frequent').fit_transform(df[enum_columns])
    if len(datetime_columns) > 0:
        df[datetime_columns] = SimpleImputer(strategy='most_frequent').fit_transform(df[datetime_columns])
    if len(string_columns) > 0:
        df[string_columns] = SimpleImputer(strategy='constant', fill_value='').fit_transform(df[string_columns])

    # Step 2: Removing Duplicates
    # Drop duplicate rows, keeping the first occurrence
    df = df.drop_duplicates()

    # # Step 3: Standardizing Data
    # # Convert all column names to lowercase and replace spaces with underscores
    # df.columns = df.columns.str.lower().str.replace(' ', '_')

    # Step 1: Handling Outliers in Numerical Columns using StandardScaler
    if len(numeric_columns) > 0:
        z_scores = np.abs(StandardScaler().fit_transform(df[numeric_columns]))
        df = df[(z_scores < 3).all(axis=1)]

    # Step 2: Handling Outliers in String Columns based on Length
    for col in string_columns:
        # Calculate the string lengths
        df[f'{col}_length'] = df[col].str.len()

        # Calculate z-scores for string lengths
        z_scores = np.abs(StandardScaler().fit_transform(df[[f'{col}_length']]))
        df = df[(z_scores < 3).all(axis=1)]

        # Drop the temporary length column
        df.drop(columns=[f'{col}_length'], inplace=True)

    # Step 3: Handling Outliers in Enum Columns based on Frequency
    for col in enum_columns:
        # Calculate the frequency of each category
        freq = df[col].value_counts()
        df[f'{col}_frequency'] = df[col].apply(lambda x: freq[x])

        z_scores = StandardScaler().fit_transform(df[[f'{col}_frequency']])
        df = df[(z_scores < 3).all(axis=1)]

        # Drop the temporary length column
        df.drop(columns=[f'{col}_frequency'], inplace=True)

    # Step 4: Handling Outliers in DateTime Columns using Timestamps
    for col in datetime_columns:
        # Convert datetime to timestamps
        df[f'{col}_timestamp'] = df[col].map(lambda x: pd.to_datetime(x) if pd.notnull(x) else np.nan)

        # Calculate z-scores for the timestamp
        z_scores = np.abs(StandardScaler().fit_transform(df[[f'{col}_timestamp']]))
        df = df[(z_scores < 3).all(axis=1)]

        # Drop the temporary timestamp column
        df.drop(columns=[f'{col}_timestamp'], inplace=True)

    # # Step 5: Handling Outliers (Optional)
    # # For example, removing outliers that are more than 3 standard deviations away
    # z_scores = np.abs(StandardScaler().fit_transform(df[numeric_columns]))
    # df = df[(z_scores < 3).all(axis=1)]

    # Step 6: Final Clean Up
    # Ensure consistency in categorical values (e.g., standardize text values)
    # df[enum_columns] = df[enum_columns].apply(lambda x: x.str.strip().str.lower().replace(' ', '_'))

    # df[string_columns] = df[string_columns].map(preprocess_text)

    df = df.dropna()

    return df
