"""add last few colums

Revision ID: 320f86691257
Revises: 69fcee9aa0a6
Create Date: 2022-09-05 19:16:33.618960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '320f86691257'
down_revision = '69fcee9aa0a6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')