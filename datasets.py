import pandas as pd
import db
import definemetrics


def get_datatypes(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.datatypes(df)


def get_statistics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.statistics(df)


def get_missingvalue(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.missingvalues(df)


def get_inconsistent_datatype(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.inconsistent_datatype(df)


def get_outlier(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.outliers(df)


def get_typos(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.typos(df)


def get_formats(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.formats(df)