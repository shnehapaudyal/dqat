# Create a SQLAlchemy engine and session
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# from aws import rds

# conf = rds.get_config()
# db_url = "postgresql://{username}:{password}@{host}:{port}/{database}".format(**conf)

db_url = "sqlite:///dataset_records.db"

print('Connecting to', db_url)
engine = create_engine(db_url, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
print('Postgres connection successful')