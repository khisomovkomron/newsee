"""add address table

Revision ID: 06e521abbd9d
Revises: fe552b926597
Create Date: 2022-11-07 22:37:00.359929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06e521abbd9d'
down_revision = 'fe552b926597'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False),
                    sa.Column('apt_num', sa.Integer(), nullable=False),)


def downgrade() -> None:
    op.drop_table('address')
