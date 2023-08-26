from typing import List

from databases import Database
from fastapi import APIRouter, Depends, HTTPException
from src import models, services
from src.dependencies import get_db

router = APIRouter()


@router.get("/balances", response_model=List[models.Balance])
async def get_balances(db: Database = Depends(get_db)):
    try:
        return await services.get_balances(db)
    except services.NoUserAccountError as e:
        raise HTTPException(status_code=404, detail=str(e))
