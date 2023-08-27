from datetime import date
from decimal import Decimal
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from src import models


@pytest.mark.asyncio
async def test_post_topup(async_client: AsyncClient) -> None:
    balance_id = 1
    dt = date(2022, 2, 1)

    test_path = f"/api/v1/topup/{balance_id}/{dt}"

    with mock.patch(
        "src.services.topup", return_value=models.Topup(balance_id=balance_id, topup_date=dt, topup_amount=Decimal(10))
    ):
        response = await async_client.post(test_path)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"balance_id": balance_id, "topup_date": "2022-02-01", "topup_amount": 10}


@pytest.mark.asyncio
async def test_get_topup(async_client: AsyncClient) -> None:
    balance_id = 1
    dt = date(2022, 2, 1)

    test_path = f"/api/v1/topup/{balance_id}/{dt}"

    with mock.patch(
        "src.services.get_topup", return_value=models.Topup(balance_id=balance_id, topup_date=dt, topup_amount=Decimal(10))
    ):
        response = await async_client.get(test_path)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"balance_id": balance_id, "topup_date": "2022-02-01", "topup_amount": 10}
