from fastapi import FastAPI
from core_files import database
from routers import country, status


app = FastAPI()

database.create_db_and_tables()


app.include_router(country.router)
app.include_router(status.router)

