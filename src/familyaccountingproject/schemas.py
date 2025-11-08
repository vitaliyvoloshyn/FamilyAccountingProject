from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel as Schema, ConfigDict


class BaseSchema(Schema):
    model_config = ConfigDict(from_attributes=True)
class UserAddDTO(BaseSchema):
    first_name: str
    last_name: str
    email: str


class UserDTO(UserAddDTO):
    id: int
    created_at: datetime | None
    is_active: bool | None


class AccountAddDTO(BaseSchema):
    name: str
    author_id: int
    currency_id: int
    account_type_id: int
    current_balance: Decimal = Decimal("0.00")


class AccountDTO(AccountAddDTO):
    id: int
    created_at: datetime
    is_active: bool
    author: 'UserDTO'
    # operations:
    currency: 'CurrencyDTO'
    # account_type:


class OperationAddDTO(BaseSchema):
    id: int
    operation_date: datetime | None = datetime.now()
    amount: Decimal
    comment: Optional[str] = None
    author_id: int
    account_id: int


class OperationDTO(OperationAddDTO):
    created_at: datetime
    updated_at: datetime
    balance_after: Decimal
    # author: 'UserDTO'
    # account: int
    # categories: List['']

class CurrencyDTO(BaseSchema):
    id: int
    name: str
    code: str
    short_form: str
