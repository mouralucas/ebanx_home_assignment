from fastapi import HTTPException
from pydantic.color import parse_str
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.account import AccountManager
from models.account import AccountModel
from schemas.account import ExecuteEventRequest, ExecuteEventResponse, AccountSchema


class AccountService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.account_manager = AccountManager(session)

    async def reset_state(self):
        await self.account_manager.reset_state()

    async def get_balance(self, account_id: str):
        account = await self.account_manager.get_account(account_id=account_id)

        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        balance = account.balance

        return balance

    async def event(self, params: ExecuteEventRequest):
        if params.event_type == 'withdraw':
            response = await self._withdraw(account_id=params.origin, amount=params.amount)
            return response

        if params.event_type == 'deposit':
            response = await self._deposit(account_id=params.destination, amount=params.amount)
            return response

        if params.event_type == 'transfer':
            response = await self._transfer(origin_account_id=params.origin, destination_account_id=params.destination, amount=params.amount)
            return response

    async def _withdraw(self, account_id: str, amount: int):
        account = await self.account_manager.get_account(account_id=account_id)
        if not account:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")

        if amount > account.balance:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        account.balance -= amount

        response = ExecuteEventResponse(
            origin=AccountSchema.model_validate(account)
        )

        return response

    async def _deposit(self, account_id: str, amount: int):
        account = await self.account_manager.get_account(account_id=account_id)
        if not account:
            account = AccountModel(
                id=account_id,
                balance=amount,
            )
            self.session.add(account)
        else:
            account.balance += amount

        response = ExecuteEventResponse(
            destination=AccountSchema.model_validate(account)
        )

        return response

    async def _transfer(self, origin_account_id: str, destination_account_id: str, amount: int):
        origin_account = await self.account_manager.get_account(origin_account_id)
        destination_account = await self.account_manager.get_account(destination_account_id)

        if not origin_account:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")


        if amount > origin_account.balance:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if not destination_account:
            destination_account = AccountModel(
                id=destination_account_id,
                balance=amount,
            )
            self.session.add(destination_account)
        else:
            destination_account.balance += amount

        origin_account.balance -= amount

        response = ExecuteEventResponse(
            origin=AccountSchema.model_validate(origin_account),
            destination=AccountSchema.model_validate(destination_account)
        )

        return response
