from datetime import date
from statistics import mean
from typing import Protocol

from src import exceptions, models


class ForecastModel(Protocol):
    def __call__(self, balance_id: int, dt: date, time_series_data: models.TimeSeriesData) -> models.Forecast:
        ...


class SevenDayAverageForecastModel(ForecastModel):
    def __call__(self, balance_id: int, dt: date, time_series_data: models.TimeSeriesData) -> models.Forecast:
        # TODO: use models.SevenDayAverageForecastInput to validate inputs

        if len(time_series_data) < 7:
            raise exceptions.NoBalanceMovementsError(f"Not enough data before {dt} to provide forecast for {balance_id=}")

        amount = mean(m.amount for m in time_series_data[-7:])

        return models.Forecast(balance_id=balance_id, forecast_date=dt, forecast_amount=amount)
