"""add archive table

Revision ID: 32ab5f3ad4c6
Revises: 1fa6af05cb68
Create Date: 2022-11-14 23:19:44.753892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32ab5f3ad4c6'
down_revision = '1fa6af05cb68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('archive',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('status', sa.Boolean()), )


def downgrade() -> None:
    op.drop_table('archive')
