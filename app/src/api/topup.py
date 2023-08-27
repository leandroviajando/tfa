from datetime import date

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, status
from src import exceptions, models, services
from src.dependencies import get_db, get_wire_transfer_service

router = APIRouter()


@router.post("/topup/{balance_id}/{dt}", status_code=status.HTTP_201_CREATED, response_model=models.Topup)
async def post_topup(
    balance_id: int,
    dt: date,
    db: Database = Depends(get_db),
    topup_service: services.TopupService = Depends(get_wire_transfer_service),
) -> models.Topup:
    try:
        return await services.topup(balance_id, dt, db=db, topup_service=topup_service)
    except (exceptions.NoBalanceMovementsError, exceptions.NotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except exceptions.AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
