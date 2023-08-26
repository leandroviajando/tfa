from fastapi import APIRouter, Depends, HTTPException
from databases import Database
from typing import List
from src import models, services
from src.dependencies import get_db

router = APIRouter()


@router.get("/balances", response_model=List[models.Balance])
async def get_account_balance(db: Database = Depends(get_db)):
    try:
        return await services.get_balances(db)
    except services.NoUserAccountError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
