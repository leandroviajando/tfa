from typing import Iterator

import pytest_asyncio
import pytest
from main import app
from httpx import AsyncClient


@pytest_asyncio.fixture
async def async_client() -> Iterator[AsyncClient]:
    await app.router.startup()
    async with AsyncClient(app=app, base_url="http://test") as async_session:
        yield async_session

    await app.router.shutdown()
