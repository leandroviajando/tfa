from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator


class AccountBalance(BaseModel):
    account_id: int
    name: str
    user_id: str
    amount: int
    created_at: datetime
    updated_at: datetime


class TransferInfo(BaseModel):
    sender_id: str
    receiver_id: str
    amount: int
    message: str
    created_at: datetime


class TransferCommand(BaseModel):
    amount: int
    # currency_code: str
    message: str
    receiver_id: str


class BalanceMovement(BaseModel):
    sending_partner_id: int
    receiving_partner_id: int
    balance_id: int
    balance_movement_amount: Decimal
    balance_movement_date: datetime


class Balance(BaseModel):
    balance_id: int
    balance_name: str = ""


class TimeSeriesData(BaseModel):
    dt: date
    amount: Decimal


class ForecastInput(BaseModel):
    balance_id: int
    forecast_date: date
    time_series_data: List[TimeSeriesData]

    @validator("time_series_data")
    def time_series_data_must_not_be_empty(cls, v: List[TimeSeriesData]) -> List[TimeSeriesData]:
        if not v:
            raise ValueError("Time series data must not be empty")
        return v

    @validator("time_series_data")
    def time_series_data_must_be_in_correct_order(cls, v: List[TimeSeriesData]) -> List[TimeSeriesData]:
        for current, next in zip(v, v[1:]):
            if next.dt < current.dt:
                raise ValueError("Time series data must be in correct order")
        return v

    @validator("forecast_date")
    def forecast_date_must_be_after_time_series_dates(cls, v: date, values: dict):
        if "time_series_data" in values and v <= values["time_series_data"][-1].dt:
            raise ValueError("Forecast date must be after time series dates")
        return v


class SevenDayAverageForecastInput(ForecastInput):
    ...

    # TODO: write custom validator to check that there are at least 7 days of data before the forecast date


class Forecast(BaseModel):
    balance_id: int
    forecast_date: date
    forecast_amount: Decimal

    class Config:
        orm_mode = True


class ForecastVarianceData(BaseModel):
    dt: date
    actual_amount: Decimal
    forecasted_amount: Decimal
    variance: Decimal
    mape: float


class ForecastVariance(BaseModel):
    balance_id: int
    from_date: Optional[date]
    to_date: Optional[date]
    data: List[ForecastVarianceData] = []
