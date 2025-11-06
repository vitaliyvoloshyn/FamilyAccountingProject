from typing import Type, Union, List

from pydantic import BaseModel as Schema
from sqlalchemy import select, Select, update, Update, delete, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from .models import Base, Operation, User, Category, Account
from .schemas import OperationDTO


class SQLAlchemyRepository:
    model: Type[Base]
    dto: Type[Schema]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, object_: Base):
        self.session.add(object_)
        await self.session.flush()
        return object_

    async def get_by_id(self, pk: int, query: Select = None):
        if not query:
            query = (select(self.model)
                     .where(self.model.id == pk))
        res = await self._execute(query)
        res_ = res.scalar()
        return res_

    async def get_list(self, validate: bool = True, **filters):
        query = select(self.model).filter_by(**filters)
        res_ = await self._execute(query)
        res = res_.scalars().all()
        if validate:
            return self.to_schema(res)
        return res

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
        return res.unique()

    async def _execute_sync(self, query: Union[Select, Update, Delete]):
        def sync_db_operation(session):
            res = session.execute(query).scalar()
            print('!!!', res)
            return res

        return await self.session.run_sync(sync_db_operation)

    def to_schema(self, list_orm: List[Base]):
        res = [self.to_schema_singleton(item) for item in list_orm]
        return res

    def to_schema_singleton(self, orm: Base):
        schema = self.dto.model_validate(orm, from_attributes=True)
        return schema


class OperationRepository(SQLAlchemyRepository):
    model = Operation
    dto = OperationDTO

    async def add(self, object_: Base, category_id: int):
        query = select(Category).where(Category.id == category_id)
        category_ = await self._execute(query)
        category = category_.scalar()
        if not category:
            raise ValueError(f'Категорії з id={category_id} не існує')
        object_.categories.append(category)
        self.session.add(object_)

    async def get_list_by_category_id(self, category_id: int):
        c = Category.__table__

        # Початковий рівень — сама категорія
        category_cte = (
            select(c.c.id, c.c.parent_id)
            .where(c.c.id == category_id)
            .cte(name="category_cte", recursive=True)
        )

        # Рекурсивна частина — беремо дочірні категорії
        category_alias = aliased(category_cte)
        category_cte = category_cte.union_all(
            select(c.c.id, c.c.parent_id).where(c.c.parent_id == category_alias.c.id)
        )

        # Вибираємо операції, прив’язані до будь-якої категорії з цього CTE
        stmt = (
            select(Operation)
            .join(Operation.categories)
            .where(Category.id.in_(select(category_cte.c.id)))
        )

        result = await self.session.scalars(stmt)
        return result.all()


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
