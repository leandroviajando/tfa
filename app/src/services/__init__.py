from datetime import date, datetime
from typing import List

import asyncpg
from databases import Database
from pydantic.tools import parse_obj_as
from sqlalchemy import select, text
from sqlalchemy.sql import func
from src import exceptions, models
from src.data import balance_movements, forecasts
from src.internal.forecast import ForecastModel


def date_to_datetime(d: date):
    return datetime(d.year, d.month, d.day)


async def get_balance_movements(
    db: Database,
    balance_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
) -> List[models.BalanceMovement]:
    query = (
        select([balance_movements])
        .select_from(balance_movements)
        .where(balance_movements.c.balance_id == balance_id)
    )

    if from_date:
        query = query.where(
            balance_movements.c.balance_movement_date >= date_to_datetime(from_date)
        )
    if to_date:
        query = query.where(
            balance_movements.c.balance_movement_date <= date_to_datetime(to_date)
        )

    rows = await db.fetch_all(query)

    return parse_obj_as(List[models.BalanceMovement], rows)


async def get_balances(db: Database):
    query = (
        select(
            balance_movements.c.balance_id,
            func.concat(text("'B-'"), balance_movements.c.balance_id).label(
                "balance_name"
            ),
        )
        .select_from(balance_movements)
        .group_by(balance_movements.c.balance_id)
    )

    rows = await db.fetch_all(query)

    return parse_obj_as(List[models.Balance], rows)


async def get_time_series(db: Database, balance_id: int, dt: date) -> List[models.TimeSeriesData]:
    query = (
        select(
            balance_movements.c.balance_movement_date.label("dt"),
            func.sum(balance_movements.c.balance_movement_amount).label("amount"),
        )
        .where(balance_movements.c.balance_id == balance_id)
        .group_by(balance_movements.c.balance_movement_date)
        .order_by(balance_movements.c.balance_movement_date)
        .where(balance_movements.c.balance_movement_date <= date_to_datetime(dt))
    )

    rows = await db.fetch_all(query)

    if not rows:
        raise exceptions.NoBalanceMovementsError(f"No balance movements before {dt} for balance_id={balance_id}")

    return parse_obj_as(List[models.TimeSeriesData], rows)


async def forecast(balance_id: int, dt: date, db: Database, forecast_model: ForecastModel) -> models.Forecast:
    forecast = forecast_model(balance_id, dt, await get_time_series(db, balance_id, dt))

    try:
        await db.execute(query=forecasts.insert(), values=forecast.dict())
    except asyncpg.exceptions.UniqueViolationError as _:
        raise exceptions.ForecastAlreadyExistsError(f"Forecast for balance_id={balance_id} and dt={dt} already exists")

    return forecast
