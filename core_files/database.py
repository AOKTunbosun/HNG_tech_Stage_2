import os
from sqlmodel import create_engine, Session
from . import models
from dotenv import load_dotenv

load_dotenv()

DB_HOST= os.getenv('DB_HOST')
DB_PORT= os.getenv('DB_PORT')
DB_USER= os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_NAME= os.getenv('DB_NAME')

# sqlite_file_name = 'database.db'
# DATABASE_URL = f'sqlite:///{sqlite_file_name}'
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session