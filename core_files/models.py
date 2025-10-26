from sqlmodel import Field, SQLModel
from pydantic import BaseModel
from datetime import datetime


class Country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    capital: str | None
    region: str | None
    population: int
    currency_code: str
    exchange_rate: float | None
    estimated_gdp: float | None
    flag_url: str | None
    last_refreshed_at: datetime


class GetCountry(BaseModel):
    pass
