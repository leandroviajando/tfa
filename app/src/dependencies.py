from typing import Generator

from databases import Database
from src.internal.database import database
from src.internal.forecast import ForecastModel, SevenDayAverageForecastModel


def get_db() -> Generator[Database, None, None]:
    yield database


def get_forecast_model() -> ForecastModel:
    return SevenDayAverageForecastModel()
