from .repository import *
from .database import async_session_factory


class StorageManager:
    """
    Асинхронний менеджер, який реалізує патерн UnitOfWork.
    Керує всіма репозиторіями, надаючи їм сесію для виконання операцій.
    Commit (або Rollback) та закриття сесії відбувається при виході з контекстного менеджера
    """
    def __init__(self):
        self.session: AsyncSession = async_session_factory()
        self.operation = OperationRepository(self.session)
        self.user = UserRepository(self.session)
        self.category = CategoryRepository(self.session)
        self.account = AccountRepository(self.session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.commit()
        except Exception as e:
            print(str(e))
            await self.session.rollback()
        finally:
            await self.session.close()
