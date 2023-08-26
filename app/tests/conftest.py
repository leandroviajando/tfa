from typing import Iterator

import pytest_asyncio
from httpx import AsyncClient
from main import app


@pytest_asyncio.fixture
async def async_client() -> Iterator[AsyncClient]:
    await app.router.startup()
    async with AsyncClient(app=app, base_url="http://test") as async_session:
        yield async_session

    await app.router.shutdown()
