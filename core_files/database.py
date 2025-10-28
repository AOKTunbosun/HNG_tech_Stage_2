import os
from sqlmodel import create_engine, Session
from . import models
from dotenv import load_dotenv

load_dotenv()


# sqlite_file_name = 'database.db'
# DATABASE_URL = f'sqlite:///{sqlite_file_name}'
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session