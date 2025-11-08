"""add test data

Revision ID: e585f9df6e8d
Revises: c5a8b1d79f98
Create Date: 2025-11-07 15:52:27.726233

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e585f9df6e8d'
down_revision: Union[str, Sequence[str], None] = 'c5a8b1d79f98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""INSERT INTO users (id, first_name, last_name, email) VALUES 
        (1, 'Віталій', 'Волошин', 'vitaliy.srt1985@gmail.com'),
        (2, 'Ольга', 'Волошина', 'voloshynaolya.edu@gmail.com')
        ;""")

    op.execute("""INSERT INTO accounts (id, name, author_id, currency_id, account_type_id) VALUES 
        (1, 'Гаманець Віталіка', 1, 1, 1),
        (2, 'Гаманець Олі', 1, 1, 1),
        (3, 'Картка Олі', 2, 1, 2),
        (4, 'Заощадження', 1, 2, 1)
        ;""")
    # Категорії витрат
    op.execute("""INSERT INTO categories (id, name, author_id, parent_id, category_type_id) VALUES 
        (1, 'Харчування', 1, Null, 2), 
        (2, 'Медикаменти', 2, Null, 2), 
        (3, 'Ремонт', 2, Null, 2), 
        (4, 'Молочні продукти', 2, 1, 2), 
        (5, 'М"ясо', 2, 1, 2), 
        (6, 'Хліб', 2, 1, 2), 
        (7, 'Полуфабрикати', 2, 1, 2)
        ;""")
    # Категорії доходу
    op.execute("""INSERT INTO categories (id, name, author_id, parent_id, category_type_id) VALUES 
        (8, 'Віталік', 1, Null, 1),
        (9, 'Оля', 1, Null, 1),
        (10, 'Заробітня плата', 2, 3, 1),
        (11, 'Заробітня плата', 2, 4, 1),
        (12, 'Репетиторство', 2, 4, 1),
        (13, 'Сдача нерухомості', 2, 4, 1),
        (14, 'Манікюр', 2, 4, 1)
        ;""")

    op.execute("""INSERT INTO operations (id, operation_date, amount, author_id, category_id, account_id, balance_after) VALUES 
        (1, '2025-09-30', 11836.89, 2, 11, 3, 11836.89),
        (2, '2025-10-30', 10636.45, 2, 11, 3, 22473.34),
        (3, '2025-11-05', 37600, 1, 10, 1, 37600)
        ;""")
    op.execute("""INSERT INTO operations (id, operation_date, amount, author_id, category_id, account_id, balance_after) VALUES 
        (4, '2025-09-30', 560, 2, 4, 3, 21913.34),
        (5, '2025-10-01', 311.74, 2, 5, 3, 21601.6),
        (6, '2025-10-02', 113.6, 2, 6, 1, 37486.4),
        (7, '2025-10-03', 947.3, 2, 7, 1, 36539.1),
        (8, '2025-10-04', 245.78, 2, 5, 3, 21355.82),
        (9, '2025-10-05', 90.5, 2, 6, 1, 36448.6),
        (10, '2025-10-06', 609.28, 2, 7, 1, 35839.32)
        ;""")

    op.execute("UPDATE accounts SET current_balance = 35839.32 WHERE accounts.id = 1;")
    op.execute("UPDATE accounts SET current_balance = 21355.82 WHERE accounts.id = 3;")



def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM users WHERE id IN (1, 2);")
    op.execute("DELETE FROM accounts WHERE id IN (1, 2, 3, 4);")
    op.execute("DELETE FROM categories WHERE id IN (1,2,3,4,5,6,7,8,9,10,11,12,13,14);")
    op.execute("DELETE FROM operations WHERE id IN (1,2,3,4,5,6,7,8,9,10);")
    op.execute("UPDATE accounts SET current_balance = 0 WHERE accounts.id = 1;")
    op.execute("UPDATE accounts SET current_balance = 0 WHERE accounts.id = 3;")
