from pydantic import BaseModel, Field


class GetBalanceSchema(BaseModel):
    account_id: int = Field(..., alias="account_id", description='The account id')
    balance: float = Field(..., alias='balance', description='The balance of the account')


class ExecuteEventRequest(BaseModel):
    event_type: str = Field(..., alias='type', description='The event type')
    origin: int = Field(..., description='The id of origin account')
    destination: int = Field(..., description='The id of destination account')
    amount: float = Field(..., description='')