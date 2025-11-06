import asyncio

from src.familyaccountingproject.models import Operation, Account
from src.familyaccountingproject.unit_of_work import StorageManager


# Run the async function

async def test_operations():
    # await operation_repository.add(Operation(amount=67,comment='opar', operation_type_id=2))
    # await operation_repository.add(Operation(amount=108,comment='ergr', operation_type_id=1))
    # await operation_repository.add(Operation(amount=345.34,comment='tr5h6jtg', operation_type_id=2))
    async with StorageManager() as sm:
        # res = await sm.user.add(User(first_name='John',
        #                        last_name='Connor',
        #                        email='connor@m.com'))
        # print(res)
        # await sm.category.add(Category(name='Харчування',
        #                                author_id=4,
        #                                category_type_id=2,
        #                                ))
        # await sm.category.add(Category(name='Медицина',
        #                                author_id=4,
        #                                category_type_id=2,
        #                                ))
        # await sm.category.add(Category(name='Молочні продукти',
        #                                author_id=4,
        #                                category_type_id=2,
        #                                parent_id=10))
        # await sm.category.add(Category(name='Молоко селянське',
        #                                author_id=4,
        #                                category_type_id=2,
        #                                parent_id=16))
        # await sm.category.add(Category(name='Зарплата',
        #                                author_id=4,
        #                                category_type_id=1,
        #                                ))
        # await sm.account.add(Account(name='Моя картка',
        #                                author_id=4,
        #                                currency_id=1,
        #                                account_type_id=2,
        #                                ))
        # await sm.operation.add(Operation(amount=47,
        #                                  author_id=4,
        #                                  account_id=2,
        #                                  ),18)
        print(await sm.operation.get_list())


if __name__ == "__main__":
    # asyncio.run(drop_db_tables())
    # asyncio.run(operation_types_repository.add(OperationType(type='Дохід')))
    asyncio.run(test_operations())
