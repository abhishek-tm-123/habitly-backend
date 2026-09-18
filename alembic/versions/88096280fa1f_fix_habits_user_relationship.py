"""fix habits user relationship

Revision ID: 88096280fa1f
Revises: 1e7d788a3926
Create Date: 2026-09-16 20:39:49.496064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '88096280fa1f'
down_revision: Union[str, Sequence[str], None] = '1e7d788a3926'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("habits")

    op.create_table(
        "habits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_habits_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_habits_id",
        "habits",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_habits_user_id",
        "habits",
        ["user_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index("ix_habits_user_id", table_name="habits")
    op.drop_index("ix_habits_id", table_name="habits")
    op.drop_table("habits")
    # ### end Alembic commands ###
