from datetime import date

from databases import Database
from fastapi import APIRouter, Depends

from src import models
from src.dependencies import get_db

router = APIRouter()


@router.get("/forecast_variance/{balance_id}", response_model=models.ForecastVariance)
def get_forecast_variance(
    balance_id: int,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Database = Depends(get_db),
):
    return models.ForecastVariance(
        balance_id=balance_id,
        from_date=from_date,
        to_date=to_date,
        data=[
            models.ForecastVarianceData(
                dt=date(2022, 1, 1),
                actual_amount=10,
                forecasted_amount=11,
                variance=1,
                mape=10,
            ),
            models.ForecastVarianceData(
                dt=date(2022, 1, 2),
                actual_amount=15,
                forecasted_amount=16,
                variance=1,
                mape=8,
            ),
        ],
    )
