import pytest
from unittest import mock
from datetime import date
from fastapi import status
from app.internal.database import database


@pytest.mark.asyncio
async def test_empty_balance_movements(async_client):
    from_date = date(2021, 10, 1)
    to_date = date(2021, 11, 1)
    balance_id = 1

    test_path = f"/api/v1/balance_movements/{balance_id}?from_date={from_date}&to_date={to_date}"

    with mock.patch(
        "app.services.get_balance_movement",
        return_value=[],
    ) as mock_get_bms:
        response = await async_client.get(test_path)

    mock_get_bms.assert_called_once_with(database, balance_id, from_date, to_date)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
