from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class AccountModel(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True)
    balance: Mapped[float] = mapped_column(default=0.0)
