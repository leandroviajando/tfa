from datetime import date

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from src import exceptions, models, services
from src.dependencies import get_db, get_forecast_model
from src.internal.forecast import ForecastModel

router = APIRouter()


@router.post("/forecast/{balance_id}/{dt}", status_code=status.HTTP_201_CREATED, response_model=models.Forecast)
async def post_forecast(
    balance_id: int, dt: date, db: Database = Depends(get_db), forecast_model: ForecastModel = Depends(get_forecast_model)
) -> models.Forecast:
    try:
        return await services.forecast(balance_id, dt, db=db, forecast_model=forecast_model)
    except exceptions.NoBalanceMovementsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except exceptions.ForecastAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
