from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import sessionmanager
from models.account import AccountModel, Base


class AccountManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def reset_state(self):
        async with sessionmanager.connect() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        # account_1 = AccountModel(id="100", balance=0)
        # account_2 = AccountModel(id="300", balance=0)
        #
        # account_list = [account_1, account_2]
        #
        # self.session.add_all(account_list)

        return True

    async def get_account(self, account_id: str):
        query = select(AccountModel).where(AccountModel.id == account_id)

        try:
            result = await self.session.execute(query)
            result = result.scalar_one()
        except Exception as e:
            result = None

        return result