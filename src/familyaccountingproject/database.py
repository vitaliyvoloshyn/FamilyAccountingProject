from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..config import db_config
from .models import Base

engine = create_async_engine(url=db_config().get_db_dsn(), echo=True)
async_session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

"""
migration for adding data
def upgrade() -> None:
    op.execute("INSERT INTO operation_types (id, type) VALUES (1, 'Дохід');")
    op.execute("INSERT INTO operation_types (id, type) VALUES (2, 'Витрата');")
    or 
    op.execute("INSERT INTO operation_types (id, type) VALUES (1, 'Дохід'),
    (1, 'Дохід');")


def downgrade() -> None:
    op.execute("DELETE FROM operation_types WHERE id IN (1, 2);")
"""

if __name__ == '__main__':
    print(type(async_session_factory))
