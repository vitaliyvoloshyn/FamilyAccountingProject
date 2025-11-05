from datetime import datetime
from decimal import Decimal
from typing import List

from sqlalchemy import String, func, DECIMAL, UniqueConstraint, Column, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, backref
from sqlalchemy.sql import expression


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True, server_default=expression.true())
    __table_args__ = (
        UniqueConstraint('email', name='unique_users_email'),
    )
    def __repr__(self):
        return f'User(id={self.id}, email={self.email})'


class Currency(Base):
    __tablename__ = 'currencies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    short_form: Mapped[str] = mapped_column(String(10))
    accounts:Mapped[List['Account']] = relationship(back_populates='currency')
    __table_args__ = (
        UniqueConstraint('name', name='unique_currencies_name'),
        UniqueConstraint('code', name='unique_currencies_code'),
    )


class AccountType(Base):
    __tablename__ = 'account_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(unique=True)
    accounts: Mapped[List['Account']] = relationship(back_populates='account_type', lazy='joined')
    __table_args__ = (
        UniqueConstraint('type', name='unique_account_types_type'),
    )


class Account(Base):
    __tablename__ = 'accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    is_active: Mapped[bool] = mapped_column(default=True, server_default=expression.true())
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', name='account-author_id'))
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id', name='account-currency_id'))
    account_type_id: Mapped[int] = mapped_column(ForeignKey('account_types.id', name='account-account_type_id'))
    author: Mapped['User'] = relationship(backref='accounts', lazy='joined')
    operations: Mapped[List['Operation']] = relationship(back_populates='account', lazy='joined')
    currency: Mapped['Currency'] = relationship(back_populates='accounts', lazy='joined')
    account_type: Mapped['AccountType'] = relationship(back_populates='accounts', lazy='joined')

    __table_args__ = (
        UniqueConstraint('name', name='unique_accounts_name'),
    )


class CategoryType(Base):
    __tablename__ = 'category_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(unique=True)
    categories: Mapped[List['Category']] = relationship(back_populates='category_type', lazy='joined')

    __table_args__ = (
        UniqueConstraint('type', name='unique_category_types_type'),
    )


category_operation = Table(
    'category_operation',
    Base.metadata,
    Column('category_id', ForeignKey('categories.id', name='category_operation-category_id'), primary_key=True),
    Column('operation_id', ForeignKey('operations.id', name='category_operation-operation_id'), primary_key=True),
)


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(backref='categories', lazy='joined')
    parent_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    category_type_id: Mapped[int] = mapped_column(ForeignKey('category_types.id'))
    operations: Mapped[List['Operation']] = relationship(secondary=category_operation,
                                                         back_populates='categories', lazy='joined')
    category_type: Mapped['CategoryType'] = relationship(back_populates='categories', lazy='joined')
    # parent: Mapped['Category'] = relationship(lazy='joined', backref=backref('parent', remote_side=[id]))
    parent: Mapped['Category'] = relationship("Category", remote_side=[id], lazy='joined')
    children: Mapped[List['Category']] = relationship("Category", back_populates='parent', lazy='joined')
    __table_args__ = (
        UniqueConstraint('name', name='unique_categories_name'),
    )

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, author={self.author}, parent_category={self.parent}, children={self.children})"


class Operation(Base):
    __tablename__ = 'operations'
    id: Mapped[int] = mapped_column(primary_key=True)
    operation_date: Mapped[datetime] = mapped_column(server_default=func.now())
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    comment: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', name='operation-user_id'))
    account_id: Mapped[int] = mapped_column(ForeignKey('accounts.id', name='operation-account_id'))
    author: Mapped['User'] = relationship(backref='operations', lazy='joined')
    account: Mapped['Account'] = relationship(back_populates='operations', lazy='joined')
    categories: Mapped[List['Category']] = relationship(secondary=category_operation,
                                                        back_populates='operations')

    def __repr__(self):
        return f"{self.__class__.__name__}(amount={self.amount}"
