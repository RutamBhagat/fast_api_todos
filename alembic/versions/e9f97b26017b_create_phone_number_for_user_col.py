"""create phone number for user col

Revision ID: e9f97b26017b
Revises: 
Create Date: 2024-02-23 02:17:20.601453

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9f97b26017b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("phone_number", sa.String(length=20), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "phone_number")
