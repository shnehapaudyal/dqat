import pandas as pd
from flask import jsonify

import db
import definemetrics
from domain import outlier, types, completeness, readability
from files import files


def get_datatypes(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return types.get_column_types(df)


def get_statistics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return definemetrics.statistics(df)


def get_missingvalue(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return completeness.missingvalues(df)


def get_inconsistent_datatype(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return definemetrics.inconsistent_datatype(df)


def get_outlier(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return outlier.outliers(df)


def get_typos(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return readability.typos(df)


def get_formats(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return definemetrics.calculate_format_validation(df)


def get_duplicate(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = files.read(dataset_path)
    return {}
    # duplicates_info = definemetrics.duplicate_records(df)
    # duplicates_info = {key: float(value) if isinstance(value, (int, float)) else value for key, value in
    #                    duplicates_info.items()}
    # return jsonify(duplicates_info)
