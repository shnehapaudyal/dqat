import json
import pickle

import pandas as pd

import db
from datasets import get_datatypes
from files import files
from domain import diversity, ease_of_manipulation
from domain import outlier, types, completeness, readability, conformity, consistency, uniqueness
from rfl import get_rfl


def get_dataset_metrics(df):
    return dataset_metrics(df)


def dataset_metrics(df):
    type_info = types.get_type_info(df)

    return [
        {'name': 'completeness', 'score': completeness.calculate_completeness(df)},
        {'name': 'uniqueness', 'score': uniqueness.calculate_uniqueness(df)},
        {'name': 'consistency', 'score': consistency.calculate_consistency(df, type_info)},
        {'name': 'conformity', 'score': conformity.calculate_conformity(df, types.supported_patterns, type_info)},
        {'name': 'readability', 'label': 'Spelling Accuracy', 'score': readability.calculate_readability(df, type_info)},
        {'name': 'ease_of_manipulation', 'score': ease_of_manipulation.calculate_ease_of_manipulation(df)},
        {'name': 'lexical_diversity', 'score': diversity.calculate_diversity(df, type_info)},
    ]


def get_dataset_dataframe(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return df


def calculate_overall_score(df):
    metrics = dataset_metrics(df)

    total_score = sum(metric['score'] for metric in metrics)

    return total_score / len(metrics)


def get_missingvalue(df):
    return completeness.missingvalues(df)


def get_inconsistent_datatype(df):
    type_info = types.get_type_info(df)
    return consistency.inconsistency(df, type_info)


def get_outlier(df):
    type_info = types.get_type_info(df)
    return outlier.outliers(df, type_info)


def get_typos(df):
    type_info = types.get_type_info(df)
    return readability.typos(df, type_info)


def get_invalid_formats(df):
    type_info = types.get_type_info(df)
    return conformity.invalid_formats(df, types.supported_patterns, type_info)


def get_duplicate(df):
    return {}
    # duplicates_info = definemetrics.duplicate_records(df)
    # duplicates_info = {key: float(value) if isinstance(value, (int, float)) else value for key, value in
    #                    duplicates_info.items()}
    # return jsonify(duplicates_info)


try:
    with open('model/estimator.pkl', 'rb') as file:
        metrics_estimator = pickle.load(file)
except Exception as e:
    print('Error', e)


def get_metrics_estimate(df):
    predicted_scores = metrics_estimator.predict(df.columns)
    for metric in predicted_scores:
        predicted_scores[metric] = float(predicted_scores[metric])
    return predicted_scores


def get_readability(df):
    rfl = pd.DataFrame()
    column_types = get_datatypes(df).to_dict(orient='list')

    def is_string(column):
        return column_types['type'][column_types['column'].index(column)] == 'string'

    for column in df.columns:
        if is_string(column):
            rfl[column] = get_rfl(df[column])

    if rfl.size > 0:
        rfl = rfl.mode()
        return rfl.to_dict(orient='records')[0]
    else:
        return {}

