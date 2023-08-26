from datetime import date, datetime
from typing import List

from databases import Database
from pydantic.tools import parse_obj_as
from sqlalchemy import select, text
from sqlalchemy.sql import func
from src import models
from src.data import balance_movements


class ErrorBase(Exception):
    """Base error"""


class NoBalanceMovementError(ErrorBase):
    """No balance movements"""


class NoUserAccountError(ErrorBase):
    """No user account"""


def date_to_datetime(d: date):
    return datetime(d.year, d.month, d.day)


async def get_balance_movements(
    db: Database,
    balance_id: int,
    from_date: date = None,
    to_date: date = None,
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
