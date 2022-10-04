"""Add user table

Revision ID: 36a8482dede8
Revises: f74a49480f16
Create Date: 2022-09-05 13:35:35.284919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36a8482dede8'
down_revision = 'f74a49480f16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
