from datetime import date, datetime
from decimal import Decimal
from logging import getLogger
from statistics import variance
from typing import List, NamedTuple, cast

import asyncpg
from databases import Database
from pydantic.tools import parse_obj_as
from sqlalchemy import select, text
from sqlalchemy.sql import func
from src import exceptions, models
from src.data import balance_movements, forecasts, receiving_partner_balances, topups
from src.internal.forecast import ForecastModel
from src.internal.topup import TopupService

logger = getLogger(__name__)


def date_to_datetime(d: date):
    return datetime(d.year, d.month, d.day)


async def get_balance_movements(
    db: Database,
    balance_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
) -> List[models.BalanceMovement]:
    query = select([balance_movements]).select_from(balance_movements).where(balance_movements.c.balance_id == balance_id)

    if from_date:
        query = query.where(balance_movements.c.balance_movement_date >= date_to_datetime(from_date))
    if to_date:
        query = query.where(balance_movements.c.balance_movement_date <= date_to_datetime(to_date))

    rows = await db.fetch_all(query)

    return parse_obj_as(List[models.BalanceMovement], rows)


async def get_balances(db: Database):
    query = (
        select(
            balance_movements.c.balance_id,
            func.concat(text("'B-'"), balance_movements.c.balance_id).label("balance_name"),
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
        raise exceptions.AlreadyExistsError(f"Forecast for balance_id={balance_id} and dt={dt} already exists")

    return forecast


async def get_forecast(balance_id: int, dt: date, db: Database) -> models.Forecast:
    query = (
        select([forecasts])
        .select_from(forecasts)
        .where(forecasts.c.balance_id == balance_id)
        .where(forecasts.c.forecast_date == dt)
    )

    row = await db.fetch_one(query)

    if not row:
        raise exceptions.NotFoundError(f"Forecast for balance_id={balance_id} and dt={dt} not found")

    return parse_obj_as(models.Forecast, row)


async def get_available_balance(balance_id: int, db: Database) -> Decimal:
    query = (
        select(receiving_partner_balances.c.available_balance)
        .where(receiving_partner_balances.c.balance_id == balance_id)
        .order_by(receiving_partner_balances.c.balance_snapshot_date.desc())
        .limit(1)
    )

    row = await db.fetch_one(query)

    if not row:
        raise exceptions.NotFoundError(f"Available balance for balance_id={balance_id} not found")

    return row.available_balance  # type: ignore


async def topup(balance_id: int, dt: date, db: Database, topup_service: TopupService) -> models.Topup:
    forecast = await get_forecast(balance_id, dt, db)
    available_balance = await get_available_balance(balance_id, db)
    topup = models.Topup(
        topup_date=dt,
        balance_id=balance_id,
        topup_amount=max(0, forecast.forecast_amount - available_balance),
    )

    async with db.transaction() as _:
        try:
            await db.execute(query=topups.insert(), values=topup.dict())
        except asyncpg.exceptions.UniqueViolationError as _:
            raise exceptions.AlreadyExistsError(f"Topup for balance_id={balance_id} and dt={dt} already exists")

        try:
            await db.execute(
                query=receiving_partner_balances.insert(),
                values={
                    "balance_id": balance_id,
                    "available_balance": available_balance + topup.topup_amount,
                    "balance_snapshot_date": dt,
                },
            )
        except asyncpg.exceptions.UniqueViolationError as _:  # noqa
            raise exceptions.AlreadyExistsError(f"Available balance for balance_id={balance_id} and dt={dt} already exists")

        await topup_service(
            models.TransferCommand(
                amount=topup.topup_amount, message=f"TOPUP balance {balance_id}", receiver_id=f"B-{balance_id}"
            )
        )

    return topup


async def get_topup(balance_id: int, dt: date, db: Database) -> models.Topup:
    query = select([topups]).select_from(topups).where(topups.c.balance_id == balance_id).where(topups.c.topup_date == dt)

    row = await db.fetch_one(query)

    if not row:
        raise exceptions.NotFoundError(f"Topup for balance_id={balance_id} and dt={dt} not found")

    return parse_obj_as(models.Topup, row)


def mape(actual: float, forecast: float) -> float:
    return abs((actual - forecast) / actual)


class ForecastVarianceRow(NamedTuple):
    forecast_date: date
    actual_amount: Decimal
    forecast_amount: Decimal


async def forecast_variance(
    db: Database,
    balance_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
) -> models.ForecastVariance:
    subquery_actual_amount = (
        select(
            balance_movements.c.balance_movement_date,
            func.sum(balance_movements.c.balance_movement_amount).label("actual_amount"),
        )
        .where(balance_movements.c.balance_id == balance_id)
        .group_by(balance_movements.c.balance_movement_date)
    )
    if from_date:
        subquery_actual_amount = subquery_actual_amount.where(
            balance_movements.c.balance_movement_date >= date_to_datetime(from_date)
        )
    if to_date:
        subquery_actual_amount = subquery_actual_amount.where(
            balance_movements.c.balance_movement_date <= date_to_datetime(to_date)
        )
    subquery_actual_amount = subquery_actual_amount.subquery()

    query = (
        select(
            forecasts.c.forecast_date,
            forecasts.c.forecast_amount,
            subquery_actual_amount.c.actual_amount,
        )
        .select_from(forecasts)
        .join(subquery_actual_amount, subquery_actual_amount.c.balance_movement_date == forecasts.c.forecast_date)
        .where(forecasts.c.balance_id == balance_id)
        .order_by(forecasts.c.forecast_date)
    )

    rows = cast(List[ForecastVarianceRow], await db.fetch_all(query))

    if not rows:
        raise exceptions.NotFoundError(
            f"Forecast or actual amounts for balance_id={balance_id} {from_date=} {to_date=} not found"
        )

    return models.ForecastVariance(
        balance_id=balance_id,
        from_date=from_date,
        to_date=to_date,
        data=[
            models.ForecastVarianceData(
                dt=row.forecast_date,
                actual_amount=row.actual_amount,
                forecast_amount=row.forecast_amount,
                variance=variance([row.actual_amount, row.forecast_amount]),
                mape=mape(float(row.actual_amount), float(row.forecast_amount)),
            )
            for row in rows
        ],
    )
