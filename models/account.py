from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[str] = mapped_column(primary_key=True)
    balance: Mapped[int] = mapped_column(default=0.0)
