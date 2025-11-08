"""add general data

Revision ID: c5a8b1d79f98
Revises: fa3bf827ec4f
Create Date: 2025-11-07 15:52:00.633322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5a8b1d79f98'
down_revision: Union[str, Sequence[str], None] = 'fa3bf827ec4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("INSERT INTO category_types (id, type) VALUES (1, 'Дохід'), (2, 'Витрата');")
    op.execute("INSERT INTO account_types (id, type) VALUES (1, 'Готівка'), (2, 'Картка'), (3, 'Борг'), (4, 'Майно');")
    op.execute("""INSERT INTO currencies (id, name, code, short_form) VALUES 
    (1, 'Українська гривня', 'UAH', 'грн'),
    (2, 'Американський долар', 'USD', '$'),
    (3, 'Євро', 'EUR', '€');""")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM category_types WHERE id IN (1, 2);")
    op.execute("DELETE FROM currencies WHERE id IN (1, 2, 3);")
    op.execute("DELETE FROM account_types WHERE id IN (1, 2, 3, 4);")
