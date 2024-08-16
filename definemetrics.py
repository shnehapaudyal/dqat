import json
import nltk
import pandas as pd
import numpy as np
import re

from domain.consistency import calculate_consistency


def get_data():
    dataset_path = ["datasets/dementia-death-rates-new.csv", "datasets/Monkeypox Coursework Dataset.csv",
                    "datasets/AppleStore.csv"]
    data_frame = pd.read_csv(dataset_path[1])
    return data_frame


# def calculate_consistency(df, schema):
#     total_values = df.size
#     consistent_values = 0
#     for column in df.columns:
#         if column in schema:
#             consistent_values += df[column].apply(lambda x: isinstance(x, schema[column])).sum()
#     consistency = (1 - consistent_values / total_values) * 100
#     return consistency


# till here Checked


# Dataset Information
def datatypes(df):
    df = df.copy()
    dtypes_dict = df.dtypes.to_dict()
    return {k: str(dtypes_dict[k]) for k in dtypes_dict.keys()}


# Dataset Problems
def inconsistent_datatype(df):
    type_mapping = {
        'int64': int,
        'float64': float,
        'object': str,
        'bool': bool,
        'datetime64[ns]': pd.Timestamp
    }
    schema = {column: type_mapping[str(dtype)] for column, dtype in df.dtypes.items()}

    column_inconsistency = {}

    for column in df.columns:
        if column in schema:
            total_values = len(df[column])
            consistent_values = df[column].apply(lambda x: isinstance(x, schema[column])).sum()
            consistency = (consistent_values / total_values) * 100
            column_inconsistency[column] = 100 - consistency

    return column_inconsistency

# if __name__ == "__main__":
#     # Example usage
#     df = get_data()
#     consistent_values = 0
#     type_mapping = {
#         'int64': int,
#         'float64': float,
#         'object': str,
#         'bool': bool,
#         'datetime64[ns]': pd.Timestamp
#     }
#     schema = {column: type_mapping[str(dtype)] for column, dtype in df.dtypes.items()}
#     formats = {"date": r"\d{4}-\d{2}-\d{2}",
#                "time": r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b",
#                "email": r"[^@]+@[^@]+\.[^@]+",
#                "zip_code": r"\b\d{5}\b",
#                "credit_card": r"\b\d{4}-?\d{4}-?\d{4}-?\d{4}\b",
#                "url": r"https?://[^\s]+",
#                "uk_postal_code": r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
#                "canadian_postal_code": r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$"
#                }

# current_date = pd.Timestamp.now()
# last_modification_date = pd.Timestamp("2023-06-01")
# creation_date = pd.Timestamp("2022-01-01")
# access_count = 150
# total_access_count = 200
# policy = True
# protocols = True
# threat_detection = True
# encryption = True
# documentation = True
# original_df = df.copy()
# processed_df = df.copy()  # Assume some preprocessing has been done
#
# completeness = calculate_completeness(df)
# uniqueness = calculate_uniqueness(df)
# consistency = calculate_consistency(df)
# conformity = calculate_conformity(df, formats)
# timeliness = calculate_timeliness(df, current_date, last_modification_date, creation_date)
# volatility = calculate_volatility(current_date, creation_date, last_modification_date)
# readability = calculate_readability(df)
# ease_of_manipulation = calculate_ease_of_manipulation(df)
# relevancy = calculate_relevancy(access_count, total_access_count)
# security = calculate_security(policy, protocols, threat_detection, encryption, documentation)
# accessibility = calculate_accessibility(df)
# integrity = calculate_integrity(df)
#
# print(f"Completeness: {completeness}%")
# print(f"Uniqueness: {uniqueness}%")
# print(f"Consistency: {consistency}%")
# print(f"Conformity: {conformity}%")
# print(f"Timeliness: {timeliness}%")
# print(f"Volatility: {volatility}%")
# print(f"Readability: {readability}%")
# print(f"Ease of Manipulation: {ease_of_manipulation}%")
# print(f"Relevancy: {relevancy}%")
# print(f"Security: {security}%")
# print(f"Accessibility: {accessibility}%")
# print(f"Integrity: {integrity}%")
# # print(f"Score
