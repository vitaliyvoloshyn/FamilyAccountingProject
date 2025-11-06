import datetime
from datetime import date
from typing import List

from pydantic import BaseModel as Schema


class UserAddDTO(Schema):
    first_name: str
    last_name: str
    email: str


class UserDTO(UserAddDTO):
    id: int
    created_at: date | None
    is_active: bool | None


class AccountAddDTO(Schema):
    name: str
    author_id: int
    currency_id: int
    account_type_id: int


class AccountDTO(AccountAddDTO):
    id: int
    created_at: date
    is_active: bool
    author: 'UserDTO'
    # operations:
    # currency:
    # account_type:


class OperationAddDTO(Schema):
    id: int
    operation_date: date | None = datetime.datetime.now().date()
    amount: int
    comment: str
    author_id: int
    account_id: int


class OperationDTO(OperationAddDTO):
    created_at: date
    updated_at: date
    author: 'UserDTO'
    account: int
    categories: List['']
