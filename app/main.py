import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.internal.database import database
from src.api import balances, forecast_variance, balance_movements

app = FastAPI(title="WalletService", openapi_url=f"/api/v1/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[url.rstrip("/") for url in ["http://localhost:8080"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    for _ in range(3):
        try:
            await database.connect()
            break
        except:
            await asyncio.sleep(1)
            continue


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(forecast_variance.router, prefix="/api/v1")
app.include_router(balances.router, prefix="/api/v1")
app.include_router(balance_movements.router, prefix="/api/v1")
