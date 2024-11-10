from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from backend.database import db_session
from schemas.account import ExecuteEventRequest
from services.account import AccountService

router = APIRouter(prefix="", tags=['Account'])


@router.post('/reset', summary='Reset database state', description='Reset database state before starting, create necessary accounts')
async def reset(
        session: AsyncSession = Depends(db_session),
):
    return await AccountService(session=session).reset_state()

@router.get('/balance', summary='Get account balance')
async def get_balance():
    pass


@router.post('/event', summary='Create event')
async def account_event(
        params: ExecuteEventRequest,
        session: AsyncSession = Depends(db_session)
):
    return AccountService(session=session).withdraw()
