from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import sessionmanager
from managers.account import AccountManager
from models.account import Base, AccountModel
from schemas.account import GetBalanceSchema, ExecuteEventRequest


class AccountService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.account_manager = AccountManager(session)

    async def reset_state(self):
        await self.account_manager.reset_state()


    async def get_balance(self, params: GetBalanceSchema):
        pass

    async def event(self, params: ExecuteEventRequest):
        if params.event_type == 'withdraw':
            response = self._withdraw()

        if params.event_type == 'deposit':
            response = self._deposit()

        if params.event_type == 'transfer':
            response = self._transfer()

    async def _withdraw(self):
        pass

    async def _deposit(self):
        pass

    async def _transfer(self):
        pass
