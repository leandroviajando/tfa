from datetime import date
from typing import List

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from src import models, services
from src.dependencies import get_db

router = APIRouter()


@router.get("/balance_movements/{balance_id}", response_model=List[models.BalanceMovement])
async def get_balance_movements(
    balance_id: int,
    from_date: date = None,
    to_date: date = None,
    db: Database = Depends(get_db),
):
    try:
        return await services.get_balance_movements(db, balance_id, from_date, to_date)
    except services.NoBalanceMovementError as e:
        raise HTTPException(status_code=404, detail=str(e))
