from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import sessionmanager
from models.account import AccountModel, Base


class AccountManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def reset_state():
        """
        Drop and then recreate all tables in database
        :return:
        """
        async with sessionmanager.connect() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        return True

    async def get_account(self, account_id: str):
        """
        Fetch the account in the database using the given account id.
        If account not found return None to be processed by the caller
        :param account_id:
        :return:
        """
        query = select(AccountModel).where(AccountModel.id == account_id)

        try:
            result = await self.session.execute(query)
            result = result.scalar_one()
        except Exception as e:
            result = None

        return result