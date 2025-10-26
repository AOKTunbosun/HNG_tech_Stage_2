import os
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List, Dict
from core_files import database, models
import requests
from datetime import datetime
import random
from sqlmodel import Session, select, delete, and_, desc
from dotenv import load_dotenv



router = APIRouter(
    prefix='/countries',
    tags=['countries']
)

get_db = database.get_session

load_dotenv()

COUNTRY_DETAILS_API = os.getenv('COUNTRY_DETAILS_API')
COUNTRY_EXCHANGE_DETAILS_API = os.getenv('COUNTRY_EXCHANGE_DETAILS_API')



@router.post('/refresh', status_code=status.HTTP_201_CREATED)
def refresh(db: Session = Depends(get_db)):
    # Retrieving all data from db
    existing_countries_query = db.exec(select(models.Country)).all()
    existing_countries_query = list(existing_countries_query)

    # Mapping country names to country data
    # For easy lookup
    existing_map = {}
    for country in existing_countries_query:
        existing_map[country.name] = country

    existing_map_keys = list(existing_map.keys())

    # Getting data from external API
    try:
        response = requests.get(COUNTRY_DETAILS_API)
        exchange_response = requests.get(COUNTRY_EXCHANGE_DETAILS_API)
        response = response.json()
        exchange_response = exchange_response.json()
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Could not fetch data from API")

    # Extracting individual data field
    for each_country in response:
        country_name = each_country.get('name')
        capital = each_country.get('capital')
        region = each_country.get('region')
        population = each_country.get('population')
        flag_url = each_country.get('flag')
        currencies = each_country.get('currencies')

        # Extracting currency code
        if currencies and isinstance(currencies, list):
            currency_info = currencies[0]
            currency_code = currency_info.get('code')

        # Getting the exchange rate
        exchange_rates = exchange_response.get('rates')
        country_rate = exchange_rates.get(f'{currency_code}')

        # Calculating GDP
        if country_rate is not None:
            estimated_gdp = int(population) * \
                random.randint(1000, 2000) / float(country_rate)
        else:
            estimated_gdp = None

        # Update and adding records section

        if country_name in existing_map_keys:
            # To Update existing records

            each_country_info = existing_map[country_name]
            if each_country_info in existing_countries_query:

                country = db.get(models.Country, each_country_info.id)

                country_data = {
                    'name': country_name,
                    'capital': capital,
                    'region': region,
                    'population': population,
                    'currency_code': currency_code,
                    'exchange_rate': country_rate,
                    'estimated_gdp': estimated_gdp,
                    'flag_url': flag_url,
                    'last_refreshed_at': datetime.now()
                }

                for field, value in country_data.items():
                    setattr(country, field, value)

                db.commit()

        else:
            # To add new record
            country_data = {
                'name': country_name,
                'capital': capital,
                'region': region,
                'population': population,
                'currency_code': currency_code,
                'exchange_rate': country_rate,
                'estimated_gdp': estimated_gdp,
                'flag_url': flag_url,
                'last_refreshed_at': datetime.now()
            }

            db_country = models.Country.model_validate(country_data)
            db.add(db_country)

        db.commit()
    # db.refresh(existing_countries_query)

    return {'detail': 'Country refresh completed'}


@router.get('', status_code=status.HTTP_200_OK)
def fetch_from_db(region: str | None = None, currency: str | None = None, sort: str | None = None, db: Session = Depends(get_db)):
    if region and not currency and not sort:
        countries = db.exec(select(models.Country).where(
            models.Country.region == region.strip().capitalize())).all()
        return countries

    elif currency and not region and not sort:
        countries = db.exec(select(models.Country).where(
            models.Country.currency_code == currency.strip().upper())).all()
        return countries

    elif sort and not region and not currency:
        if sort.strip().lower() == 'gdp_desc':
            countries = db.exec(select(models.Country).order_by(
                desc(models.Country.estimated_gdp))).all()
            return countries

        elif sort.strip().lower() == 'gdp_asc':
            countries = db.exec(select(models.Country).order_by(
                models.Country.estimated_gdp)).all()
            return countries

    else:
        countries = db.exec(select(models.Country)).all()
        return countries


@router.get('/{name}', status_code=status.HTTP_200_OK, response_model=models.Country)
def single_country_by_name(name: str, db: Session = Depends(get_db)):

    statement = select(models.Country).where(
        models.Country.name == name.strip().capitalize())
    country = db.exec(statement).first()
    # country.model_dump()

    if country.currency_code is None or country.population is None:
        if country.currency_code is None and country.population is None:

            return {'error': 'Validation failed',
                    'details': {'currency_code': 'is required', 'population': 'is required'}
                    }, status.HTTP_400_BAD_REQUEST
        elif country.currency_code is None:
            return {'error': 'Validation failed',
                    'details': {'currency_code': 'is required'}
                    }, status.HTTP_400_BAD_REQUEST
        elif country.population is None:
            return {'error': 'Validation failed',
                    'details': {'population': 'is required'}
                    }, status.HTTP_400_BAD_REQUEST

    elif country:
        return country
    elif country is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Country not found')


@router.delete('/{name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_country(name: str, db: Session = Depends(get_db)):
    country = db.exec(select(models.Country).where(
        models.Country.name == name.strip().capitalize())).first()
    if country:
        db.exec(delete(models.Country).where(
            models.Country.name == name.strip().capitalize()))
        db.commit()
        return {'detail': f"{name}'s record deleted"}

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/image')
def serve_image():
    pass
