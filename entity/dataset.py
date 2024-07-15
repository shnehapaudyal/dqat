from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

import db
from dbengine import Base


class DatasetRecord(Base):
    __tablename__ = 'dataset_records'

    dataset_id = Column(String, unique=True, primary_key=True)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    file_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)

    def __init__(self, dataset_id, filename, path, file_type, size):
        self.dataset_id = dataset_id
        self.filename = filename
        self.path = path
        self.file_type = file_type
        self.size = size

    def save(self):
        db.save_dataset(self)

    def json(self):
        return {
            'dataset_id': self.dataset_id,
            'filename': self.filename,
            'path': self.path,
            'created_at': str(self.created_at),
            'file_type': self.file_type,
            'size': self.size
        }
