"""add column to posts table

Revision ID: 6a4832d48af8
Revises: 6aa39898f6b2
Create Date: 2025-07-11 21:07:00.240800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a4832d48af8'
down_revision: Union[str, Sequence[str], None] = '6aa39898f6b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column( 'posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")) )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    pass
