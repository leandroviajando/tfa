from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError
from src import models


def test_time_series_data_must_not_be_empty():
    with pytest.raises(ValidationError):
        models.ForecastInput(
            balance_id=1,
            forecast_date=date(2023, 8, 27),
            time_series_data=[],
        )

    models.ForecastInput(
        balance_id=1,
        forecast_date=date(2023, 8, 27),
        time_series_data=[models.TimeSeriesData(dt=date(2023, 8, 26), amount=Decimal(10))],
    )

    models.ForecastInput(
        balance_id=1,
        forecast_date=date(2023, 8, 27),
        time_series_data=[
            models.TimeSeriesData(dt=date(2023, 8, 25), amount=Decimal(10)),
            models.TimeSeriesData(dt=date(2023, 8, 26), amount=Decimal(10)),
        ],
    )


def test_time_series_data_must_be_in_correct_order():
    with pytest.raises(ValidationError):
        models.ForecastInput(
            balance_id=1,
            time_series_data=[
                models.TimeSeriesData(dt=date(2023, 8, 26), amount=Decimal(300)),
                models.TimeSeriesData(dt=date(2023, 8, 25), amount=Decimal(100)),
            ],
            forecast_date=date(2023, 8, 27),
        )
