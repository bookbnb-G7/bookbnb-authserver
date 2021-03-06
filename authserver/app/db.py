import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


ENVIRONMENT = os.getenv("ENVIRONMENT")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
session = None

if ENVIRONMENT == "production":
    # use postgresql
    engine = create_engine(DATABASE_URL)

if ENVIRONMENT == "development":
    # use sqlite
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Create a Base class for models
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
