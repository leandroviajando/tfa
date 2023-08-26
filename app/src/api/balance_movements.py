from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases import Database
from typing import List
from src import models, services
from src.dependencies import get_db
from datetime import date


router = APIRouter()


@router.get("/balance_movements/{balance_id}", response_model=List[models.BalanceMovement])
async def get_balance_movement(
    balance_id: int,
    from_date: date = None,
    to_date: date = None,
    db: Database = Depends(get_db),
):
    try:
        return await services.get_balance_movement(db, balance_id, from_date, to_date)
    except services.NoBalanceMovementError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
