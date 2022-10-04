"""redo post table from scratch

Revision ID: 69fcee9aa0a6
Revises: 36a8482dede8
Create Date: 2022-09-05 13:43:46.898599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69fcee9aa0a6'
down_revision = '36a8482dede8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_id', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_user_id', table_name='posts')
    op.drop_column('posts', 'user_id')
