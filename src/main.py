import asyncio
import datetime
from pprint import pprint

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
        await sm.operation.add(Operation(amount=839,
                                         author_id=1,
                                         account_id=1,
                                         balance_after=35000.32,
                                         operation_date=datetime.datetime(2025,11,7, 15, 9, 50)
                                         ),6)
        # pprint(await sm.operation.get_list())
        # accounts = await sm.account.get_list()
        # for account in accounts:
        #     pprint(f"{account.name} - balance {account.current_balance} {account.currency.short_form}")


if __name__ == "__main__":
    # asyncio.run(drop_db_tables())
    # asyncio.run(operation_types_repository.add(OperationType(type='Дохід')))
    asyncio.run(test_operations())
