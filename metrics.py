import pandas as pd
import db
from config import *
from domain.completeness import calculate_completeness
from domain.conformity import calculate_conformity
from domain.consistency import calculate_consistency
from domain.ease_of_manipulation import calculate_ease_of_manipulation
from domain.readability import calculate_readability
from domain.timeliness import calculate_timeliness
from domain.uniqueness import calculate_uniqueness
from domain.volatility import calculate_volatility
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


    return {
        'completeness': completeness,
        'uniqueness': uniqueness,
        'consistency': consistency,
        'conformity': conformity,
        'timeliness': timeliness,
        'volatility': volatility,
        'readability': readability,
        'ease_of_manipulation': ease_of_manipulation,
    }


def calculate_overall_score(dataset_id):
    dataset_metrics = get_dataset_metrics(dataset_id)

    total_score = sum(dataset_metrics[metric] for metric in dataset_metrics.keys())

    return total_score / len(dataset_metrics)
