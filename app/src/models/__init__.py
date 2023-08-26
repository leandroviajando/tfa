from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


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
