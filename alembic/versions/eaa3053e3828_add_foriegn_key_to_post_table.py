"""add foriegn key to post table

Revision ID: eaa3053e3828
Revises: 9fddf75e2e42
Create Date: 2025-07-11 21:34:00.264127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaa3053e3828'
down_revision: Union[str, Sequence[str], None] = '9fddf75e2e42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_owner_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_owner_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
