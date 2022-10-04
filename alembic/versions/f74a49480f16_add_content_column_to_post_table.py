"""Add content column to post table

Revision ID: f74a49480f16
Revises: de5fb8931aa9
Create Date: 2022-09-05 13:30:54.047127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f74a49480f16'
down_revision = 'de5fb8931aa9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
