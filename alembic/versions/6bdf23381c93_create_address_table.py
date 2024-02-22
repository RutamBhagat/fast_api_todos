"""create address table

Revision ID: 6bdf23381c93
Revises: e9f97b26017b
Create Date: 2024-02-23 02:33:36.333658

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6bdf23381c93"
down_revision: Union[str, None] = "e9f97b26017b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "addresses",
        sa.Column(
            "id", sa.Integer(), nullable=False, primary_key=True, autoincrement=True
        ),
        sa.Column("address1", sa.String(length=100), nullable=True),
        sa.Column("address2", sa.String(length=100), nullable=True),
        sa.Column("city", sa.String(length=50), nullable=True),
        sa.Column("state", sa.String(length=50), nullable=True),
        sa.Column("country", sa.String(length=50), nullable=True),
        sa.Column("postalcode", sa.String(length=15), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("addresses")
