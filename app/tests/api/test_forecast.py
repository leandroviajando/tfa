from datetime import date
from decimal import Decimal
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from src import models


@pytest.mark.asyncio
async def test_forecast(async_client: AsyncClient) -> None:
    balance_id = 1
    forecast_date = date(2022, 2, 1)

    test_path = f"/api/v1/forecast/{balance_id}/{forecast_date}"

    with mock.patch(
        "src.services.forecast",
        return_value=models.Forecast(balance_id=balance_id, forecast_date=forecast_date, forecast_amount=Decimal(10)),
    ):
        response = await async_client.post(test_path)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"balance_id": balance_id, "forecast_date": "2022-02-01", "forecast_amount": 10}
