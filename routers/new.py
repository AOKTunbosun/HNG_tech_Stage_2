from core_files import database, models
from sqlmodel import Session, select
from fastapi import Depends, APIRouter
from typing import Dict


router = APIRouter(
    prefix='/test',
    tags=['test']
)

get_db = database.get_session

@router.get('')
def refresh(db: Session = Depends(get_db)):
    existing_countries_query = db.exec(select(models.Country)).all()

    existing_map = {}
    for country in existing_countries_query:
        existing_map[country.name] = country
        # existing_map.update
    # existing_map = dict(str, models.Country) = {c.name: c for c in existing_countries_query}
    # print(existing_map)
    keys = list(existing_map.keys())
    
    # return existing_map
    return existing_countries_query

@router.get('/give')
def give_single(id: int,db: Session = Depends(get_db)):
    single = db.exec(select(models.Country).where(models.Country.id == id)).first()
    return single
    