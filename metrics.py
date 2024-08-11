import pandas as pd
import db
import domain.types
from config import *
from domain.completeness import calculate_completeness
from domain.conformity import calculate_conformity
from domain.consistency import calculate_consistency
from domain.diversity import calculate_diversity
from domain.ease_of_manipulation import calculate_ease_of_manipulation
from domain.readability import calculate_readability
from domain.timeliness import calculate_timeliness
from domain.uniqueness import calculate_uniqueness
from domain.volatility import calculate_volatility
from files import files


def get_dataset_metrics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)

    type_info = domain.types.get_type_info(df)

    completeness = calculate_completeness(df)
    uniqueness = calculate_uniqueness(df)
    consistency = calculate_consistency(df, type_info)
    conformity = calculate_conformity(df, domain.types.supported_patterns, type_info)
    readability = calculate_readability(df, type_info)
    diversity = calculate_diversity(df, type_info)
    ease_of_manipulation = calculate_ease_of_manipulation(df)

    return [
        {'name': 'completeness', 'score': completeness},
        {'name': 'uniqueness', 'score': uniqueness},
        {'name': 'consistency', 'score': consistency},
        {'name': 'conformity', 'score': conformity},
        {'name': 'readability', 'score': readability},
        {'name': 'ease_of_manipulation', 'score': ease_of_manipulation},
        {'name': 'lexical_diversity', 'score': diversity},
    ]


def calculate_overall_score(dataset_id):
    dataset_metrics = get_dataset_metrics(dataset_id)

    total_score = sum(metric['score'] for metric in dataset_metrics)

    return total_score / len(dataset_metrics)
