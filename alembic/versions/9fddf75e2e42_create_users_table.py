"""create users table

Revision ID: 9fddf75e2e42
Revises: 6a4832d48af8
Create Date: 2025-07-11 21:27:28.963226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fddf75e2e42'
down_revision: Union[str, Sequence[str], None] = '6a4832d48af8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password', sa.String(128), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
