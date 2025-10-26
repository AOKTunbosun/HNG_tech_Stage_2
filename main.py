from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from core_files import database, models
from routers import country, status, new


app = FastAPI()

database.create_db_and_tables()


app.include_router(country.router)
app.include_router(status.router)
app.include_router(new.router)


# @app.post('/', response_model=models.Country)
# def new(request: models.GetCountry, db: Session = Depends(get_db)):
#     db_country = models.Country.model_validate(request)
#     db.add(db_country)
#     db.commit()
#     db.refresh(db_country)
#     return db_country

# @app.get('/')
# def get_all(db: Session = Depends(get_db)):
#     countries = db.exec(select(models.Country)).all()
#     return countries

# @app.get('/single')
# def get_one(id: int,db: Session = Depends(get_db)):
#     country = db.get(models.Country, id)
#     return country

# @app.put('/single')
# def update(id: int, request: models.Country, db: Session = Depends(get_db)):
#     country = db.get(models.Country, id)

#     for field, value in request.model_dump().items():
#         setattr(country, field, value)
    
#     db.commit()
#     db.refresh(country)
#     return country
