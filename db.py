# Create the table in the database
from functools import lru_cache
from dbengine import Base, engine, session
from entity.dataset import DatasetRecord

Base.metadata.create_all(engine)


def create_dataset(dataset):
    session.add(dataset)
    session.commit()


datasets = {}


def read_dataset(dataset_id):
    if dataset_id in datasets:
        return datasets[dataset_id]

    first = session.query(DatasetRecord).filter_by(dataset_id=dataset_id).first()
    datasets[dataset_id] = first
    return first


def update_dataset(dataset):
    session.merge(dataset)
    session.commit()


def delete_dataset(dataset):
    session.delete(dataset)
    session.commit()


def save_dataset(dataset):
    existing_dataset = session.query(DatasetRecord).filter_by(dataset_id=dataset.dataset_id).first()
    if existing_dataset:
        # Update existing dataset
        update_dataset(dataset)
    else:
        # Insert new dataset
        session.add(dataset)
    session.commit()


def get_all_datasets(page=0, per_page=10):
    query = session.query(DatasetRecord)

    if page < 1:
        datasets = query.all()
    else:
        datasets = query.offset((page - 1) * per_page).limit(per_page).all()

    return datasets
