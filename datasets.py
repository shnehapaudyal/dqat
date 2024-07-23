import pandas as pd
import db
import definemetrics

def get_statistics(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.statistics(df)


def get_datatypes(dataset_id):
    dataset_path = db.read_dataset(dataset_id).path
    df = pd.read_csv(dataset_path)
    return definemetrics.datatypes(df)