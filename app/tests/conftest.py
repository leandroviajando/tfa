from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    await app.router.startup()

    async with AsyncClient(app=app, base_url="http://test") as async_session:
        yield async_session

    await app.router.shutdown()
