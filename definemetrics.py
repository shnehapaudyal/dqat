import pandas as pd
import numpy as np


def get_data():
    dataset_path = ["datasets\dementia-death-rates new.csv", "datasets\AppleStore.csv"]
    data_frame = pd.read_csv(dataset_path[1])
    return data_frame

#
# def metrics(data_frame):
#     statistics = data_frame.describe()
#     info_type = data_frame.info()
#     return statistics, info_type
#
#
# data_frame = get_data()
# statistics, info_type = metrics(data_frame)
# print(statistics)
# print(info_type)

def calculate_completeness(df):
    total_values = df.size
    non_empty_values = df.notna().sum().sum()
    completeness = (non_empty_values / total_values) * 100
    return completeness

def calculate_uniqueness(df):
    total_rows = len(df)
    unique_rows = len(df.drop_duplicates())
    uniqueness = (unique_rows / total_rows) * 100
    return uniqueness

def calculate_consistency(df, schema):
    total_values = df.size
    consistent_values = 0
    for column in df.columns:
        if column in schema:
            consistent_values += df[column].apply(lambda x: isinstance(x, schema[column])).sum()
    consistency = (consistent_values / total_values) * 100
    return consistency

def calculate_conformity(df, formats):
    total_values = df.size
    conforming_values = 0
    for column in df.columns:
        if column in formats:
            conforming_values += df[column].apply(lambda x: bool(formats[column].match(str(x)))).sum()
    conformity = (conforming_values / total_values) * 100
    return conformity

def calculate_timeliness(df, current_date, last_modification_date, creation_date):
    timeliness = (current_date - last_modification_date) / (current_date - creation_date) * 100
    return timeliness

def calculate_volatility(current_date, creation_date, modification_date):
    volatility = (creation_date - modification_date) / (current_date - creation_date) * 100
    return volatility

def calculate_readability(df):
    total_values = df.size
    processed_values = df.map(lambda x: isinstance(x, (str, int, float))).sum().sum()
    readability = (processed_values / total_values) * 100
    return readability

def calculate_ease_of_manipulation(df, cleaned_df):
    differences = (df != cleaned_df).sum().sum()
    total_values = df.size
    ease_of_manipulation = (differences / total_values) * 100
    return ease_of_manipulation

def calculate_relevancy(access_count, total_access_count):
    relevancy = (access_count / total_access_count) * 100
    return relevancy

def calculate_security(policy, protocols, threat_detection, encryption, documentation):
    security = sum([policy, protocols, threat_detection, encryption, documentation]) / 5 * 100
    return security

def calculate_accessibility(df):
    total_values = df.size
    accessible_values = df.notna().sum().sum()  # Simplified assumption
    accessibility = (accessible_values / total_values) * 100
    return accessibility

def calculate_integrity(original_df, processed_df):
    differences = (original_df != processed_df).sum().sum()
    total_values = original_df.size
    integrity = (differences / total_values) * 100
    return integrity

# Example usage
df = get_data()
schema = {"column1": int, "column2": str}  # Define your schema
formats = {"date": r"\d{4}-\d{2}-\d{2}", "email": r"[^@]+@[^@]+\.[^@]+"}  # Define your formats
current_date = pd.Timestamp.now()
last_modification_date = pd.Timestamp("2023-06-01")
creation_date = pd.Timestamp("2022-01-01")
access_count = 150
total_access_count = 200
policy = True
protocols = True
threat_detection = True
encryption = True
documentation = True
original_df = df.copy()
processed_df = df.copy()  # Assume some preprocessing has been done

completeness = calculate_completeness(df)
uniqueness = calculate_uniqueness(df)
consistency = calculate_consistency(df, schema)
conformity = calculate_conformity(df, formats)
timeliness = calculate_timeliness(df, current_date, last_modification_date, creation_date)
volatility = calculate_volatility(current_date, creation_date, last_modification_date)
readability = calculate_readability(df)
ease_of_manipulation = calculate_ease_of_manipulation(df, processed_df)
relevancy = calculate_relevancy(access_count, total_access_count)
security = calculate_security(policy, protocols, threat_detection, encryption, documentation)
accessibility = calculate_accessibility(df)
integrity = calculate_integrity(original_df, processed_df)

print(f"Completeness: {completeness}%")
print(f"Uniqueness: {uniqueness}%")
print(f"Consistency: {consistency}%")
print(f"Conformity: {conformity}%")
print(f"Timeliness: {timeliness}%")
print(f"Volatility: {volatility}%")
print(f"Readability: {readability}%")
print(f"Ease of Manipulation: {ease_of_manipulation}%")
print(f"Relevancy: {relevancy}%")
print(f"Security: {security}%")
print(f"Accessibility: {accessibility}%")
print(f"Integrity: {integrity}%")
