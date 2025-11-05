from typing import Type, Union

from sqlalchemy import select, Select, update, Update, delete, Delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base, Operation, User, Category, Account


class SQLAlchemyRepository:
    model: Type[Base]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, object_):
        self.session.add(object_)
        await self.session.flush()
        return object_

    async def get_by_id(self, pk: int, query: Select = None):
        if not query:
            query = (select(self.model)
                     .where(self.model.id == pk))
        res = await self._execute(query)
        res_ = res.scalar()
        print(res_)
        return res_

    async def get_list(self, **filters):
        query = select(self.model).filter_by(**filters)
        res = await self._execute(query)
        return res.scalars().all()

    async def update(self, pk: int, **data):
        stmt = (
            update(self.model)
            .where(self.model.id == pk)
            .values(**data)
        )
        await self._execute(stmt)

    async def remove(self, pk: int):
        stmt = delete(self.model).where(self.model.id == pk)
        await self._execute(stmt)

    async def _execute(self, query: Union[Select, Update, Delete]):
        res = await self.session.execute(query)
        print(res)
        return res

    async def _execute_sync(self, query: Union[Select, Update, Delete]):
        def sync_db_operation(session):
            res = session.execute(query).scalar()
            print('!!!', res)
            return res

        return await self.session.run_sync(sync_db_operation)


class OperationRepository(SQLAlchemyRepository):
    model = Operation


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_by_email(self, email: str):
        query = select(self.model).filter_by(email=email)
        res = await self._execute(query)
        return res.scalar()


class CategoryRepository(SQLAlchemyRepository):
    model = Category

    async def get_by_id(self, pk: int, query: Select = None):
        if not query:
            query = (select(self.model)
                     .where(self.model.id == pk))
        res = await self._execute_sync(query)
        # res_ = res.scalar()
        return res


class AccountRepository(SQLAlchemyRepository):
    model = Account

    async def add(self, object_, category_id: int):
        query = select(Category).where(Category.id==category_id)
        category = await self.get_by_id(category_id, query)
        object_.category = category
        self.session.add(object_)