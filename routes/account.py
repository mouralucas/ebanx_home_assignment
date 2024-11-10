from decimal import Decimal

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from watchfiles import awatch

from backend.database import db_session
from schemas.account import ExecuteEventRequest, GetBalanceSchema, ExecuteEventResponse
from services.account import AccountService

router = APIRouter(prefix="", tags=['Account'])


@router.post('/reset', summary='Reset database state', description='Reset database state before starting')
async def reset(
        session: AsyncSession = Depends(db_session),
):
    await AccountService(session=session).reset_state()
    return Response(content="OK")

@router.get('/balance', summary='Get account balance')
async def get_balance(
        params: GetBalanceSchema = Depends(),
        session: AsyncSession = Depends(db_session),
):
    return await AccountService(session=session).get_balance(account_id=params.account_id)


@router.post('/event', summary='Create event', response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def account_event(
        params: ExecuteEventRequest,
        session: AsyncSession = Depends(db_session)
) -> ExecuteEventResponse:
    return await AccountService(session=session).event(params)
