import pandas as pd
import db
from config import *
from definemetrics import calculate_completeness, calculate_uniqueness, calculate_consistency, calculate_conformity, \
    calculate_timeliness, calculate_volatility, calculate_readability, calculate_ease_of_manipulation, \
    calculate_relevancy, calculate_security, calculate_accessibility, calculate_integrity
from files import files


def get_dataset_metrics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    completeness = calculate_completeness(df)
    uniqueness = calculate_uniqueness(df)
    consistency = calculate_consistency(df)
    conformity = calculate_conformity(df, formats)
    timeliness = calculate_timeliness(df, current_date, last_modification_date, creation_date)
    volatility = calculate_volatility(current_date, creation_date, last_modification_date)
    readability = calculate_readability(df)
    ease_of_manipulation = calculate_ease_of_manipulation(df)
    relevancy = calculate_relevancy(access_count, total_access_count)
    security = calculate_security(policy, protocols, threat_detection, encryption, documentation)
    accessibility = calculate_accessibility(df)
    integrity = calculate_integrity(df)

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
        'integrity': integrity,
    }


def calculate_overall_score(dataset_id):
    dataset_metrics = get_dataset_metrics(dataset_id)

    metrics = [
        "completeness",
        "uniqueness",
        "consistency",
        "conformity",
        "timeliness",
        "readability",
        "ease_of_manipulation",
        "integrity"
    ]

    total_score = sum(dataset_metrics[metric] for metric in metrics)

    return total_score / len(metrics)
