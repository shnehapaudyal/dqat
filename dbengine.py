# Create a SQLAlchemy engine and session
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///dataset_records.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()