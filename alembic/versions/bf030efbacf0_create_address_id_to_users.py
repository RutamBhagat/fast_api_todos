"""create address_id to users

Revision ID: bf030efbacf0
Revises: 6bdf23381c93
Create Date: 2024-02-23 02:41:32.416178

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bf030efbacf0"
down_revision: Union[str, None] = "6bdf23381c93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "addess_users_fk",
        source_table="users",
        referent_table="addresses",
        local_cols=["address_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("addess_users_fk", table_name="users", type_="foreignkey")
    op.drop_column("users", "address_id")
