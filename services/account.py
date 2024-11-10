from fastapi import HTTPException
from pydantic.color import parse_str
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from managers.account import AccountManager
from models.account import AccountModel
from schemas.account import ExecuteEventRequest, ExecuteEventResponse, AccountSchema


class AccountService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.account_manager = AccountManager(session)

    async def reset_state(self):
        """
        Drop and recreate all tables in the database generating a clean slate
        :return:
        """
        await self.account_manager.reset_state()

    async def get_balance(self, account_id: str):
        """
        Get the balance of a given account id, if account not exist raise error
        :param account_id:
        :return:
        """
        account = await self.account_manager.get_account(account_id=account_id)

        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        balance = account.balance

        return balance

    async def event(self, params: ExecuteEventRequest):
        """
        Handles account events and sends them to the appropriate method.
        :param params:
        :return:
        """
        if params.event_type == 'withdraw':
            response = await self._withdraw(account_id=params.origin_account_id, amount=params.amount)
            return response

        if params.event_type == 'deposit':
            response = await self._deposit(account_id=params.destination_account_id, amount=params.amount)
            return response

        if params.event_type == 'transfer':
            response = await self._transfer(origin_account_id=params.origin_account_id, destination_account_id=params.destination_account_id, amount=params.amount)
            return response

    async def _withdraw(self, account_id: str, amount: int):
        """
        Handles the withdrawal operation.
        If the account is not exist raise error
        If amount to withdraw is greater than the balance raise an error
        :param account_id:
        :param amount:
        :return:
        """
        account = await self.account_manager.get_account(account_id=account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if amount > account.balance:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="Insufficient funds for the withdrawal")

        account.balance -= amount

        response = ExecuteEventResponse(
            origin=AccountSchema.model_validate(account)
        )

        return response

    async def _deposit(self, account_id: str, amount: int):
        """
        Handles the deposit operation.
        If the account does not exist creates a new with the provided ID and amount.
        :param account_id:
        :param amount:
        :return:
        """
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
        """
        Handles the transfer operation.
        If the origin account does not exist raises an error.
        If the destination account does create a new account with provided ID and amount.
        :param origin_account_id:
        :param destination_account_id:
        :param amount:
        :return:
        """
        origin_account = await self.account_manager.get_account(origin_account_id)
        destination_account = await self.account_manager.get_account(destination_account_id)

        if not origin_account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if amount > origin_account.balance:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Insufficient funds for the transfer")

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
