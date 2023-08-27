from datetime import date
from decimal import Decimal
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from src import models


@pytest.mark.asyncio
async def test_get_forecast_variance(async_client: AsyncClient) -> None:
    balance_id = 1
    from_date = date(2022, 2, 1)
    to_date = date(2022, 2, 2)

    test_path = f"/api/v1/forecast_variance/{balance_id}?from_date={from_date}&to_date={to_date}"

    with mock.patch(
        "src.services.forecast_variance",
        return_value=models.ForecastVariance(
            balance_id=balance_id,
            from_date=from_date,
            to_date=to_date,
            data=[
                models.ForecastVarianceData(
                    dt=date(2022, 2, 1),
                    actual_amount=Decimal(10),
                    forecast_amount=Decimal(20),
                    variance=Decimal(10),
                    mape=Decimal(50),
                )
            ],
        ),
    ):
        response = await async_client.get(test_path)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "balance_id": balance_id,
        "from_date": "2022-02-01",
        "to_date": "2022-02-02",
        "data": [{"dt": "2022-02-01", "actual_amount": 10, "forecast_amount": 20, "variance": 10, "mape": 50}],
    }
