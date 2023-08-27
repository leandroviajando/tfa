from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List
from unittest import mock

import pytest
from fastapi import status
from httpx import AsyncClient
from src.internal.database import database
from src.models import BalanceMovement


@pytest.mark.parametrize(
    "mock_return_value, expected",
    [
        ([], []),
        (
            [
                BalanceMovement(
                    balance_id=1,
                    sending_partner_id=2,
                    receiving_partner_id=3,
                    balance_movement_amount=Decimal(10),
                    balance_movement_date=datetime(2023, 8, 27),
                )
            ],
            [
                {
                    "balance_id": 1,
                    "sending_partner_id": 2,
                    "receiving_partner_id": 3,
                    "balance_movement_amount": 10,
                    "balance_movement_date": "2023-08-27T00:00:00",
                }
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_balance_movements(
    async_client: AsyncClient, mock_return_value: List[BalanceMovement], expected: List[Dict]
):
    from_date = date(2021, 10, 1)
    to_date = date(2021, 11, 1)
    balance_id = 1

    test_path = f"/api/v1/balance_movements/{balance_id}?from_date={from_date}&to_date={to_date}"

    with mock.patch("src.services.get_balance_movements", return_value=mock_return_value) as mock_get_bms:
        response = await async_client.get(test_path)

    mock_get_bms.assert_called_once_with(database, balance_id, from_date, to_date)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected
