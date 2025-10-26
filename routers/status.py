from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from datetime import datetime
from core_files import database, models



router = APIRouter(
    prefix='/status',
    tags=['status']
)

get_db = database.get_session



@router.get('', status_code=status.HTTP_200_OK)
def status(db: Session = Depends(get_db)):
    countries = db.exec(select(models.Country)).all()
    country = countries[0]
    last_refreshed_at = country.last_refreshed_at
    total_countries = len(countries)
    return {'total_countries': total_countries,
            'last_refreshed_at': last_refreshed_at
            }
