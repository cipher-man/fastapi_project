"""add few columns

Revision ID: d9bddf10846e
Revises: eaa3053e3828
Create Date: 2025-07-11 21:41:26.432492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9bddf10846e'
down_revision: Union[str, Sequence[str], None] = 'eaa3053e3828'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.text("True")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    pass
