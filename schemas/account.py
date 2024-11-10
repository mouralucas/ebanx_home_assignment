from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class AccountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description='The account id')
    balance: int = Field(..., description='The account balance')

class GetBalanceSchema(BaseModel):
    account_id: str = Field(..., alias="account_id", description='The account id')


class ExecuteEventRequest(BaseModel):
    event_type: Literal['withdraw', 'deposit', 'transfer'] = Field(..., alias='type', description='The event type, It can by one of \'withdraw\', \'deposit\' or \'transfer\'')
    origin_account_id: str | None = Field(None, alias='origin', description='The id of origin account')
    destination_account_id: str | None = Field(None, alias='destination', description='The id of destination account')
    amount: int = Field(..., description='The amount of the operation')


class ExecuteEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    origin: AccountSchema | None = Field(None, alias='origin', description='The id of origin account')
    destination: AccountSchema | None = Field(None, alias='destination', description='The id of destination account')