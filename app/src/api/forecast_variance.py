from datetime import date

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from src import exceptions, models, services
from src.dependencies import get_db

router = APIRouter()


@router.get("/forecast_variance/{balance_id}", response_model=models.ForecastVariance)
async def get_forecast_variance(
    balance_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Database = Depends(get_db),
) -> models.ForecastVariance:
    try:
        return await services.forecast_variance(db, balance_id, from_date, to_date)
    except exceptions.NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
