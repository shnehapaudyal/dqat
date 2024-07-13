import pandas as pd
import db
from definemetrics import calculate_completeness, calculate_uniqueness, calculate_consistency, calculate_conformity, \
    calculate_timeliness, calculate_volatility, calculate_readability, calculate_ease_of_manipulation, \
    calculate_relevancy, calculate_security, calculate_accessibility, calculate_integrity


def get_dataset_metrics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)

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

    return {
        'completeness': completeness,
        'uniqueness': uniqueness,
        'consistency': consistency,
        'conformity': conformity,
        'timeliness': timeliness,
        'volatility': volatility,
        'readability': readability,
        'ease_of_manipulation': ease_of_manipulation,
        'relevancy': relevancy,
        'security': security,
        'accessibility': accessibility,
        'integrity': integrity
    }