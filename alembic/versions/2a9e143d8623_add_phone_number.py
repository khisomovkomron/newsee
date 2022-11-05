"""add phone_number

Revision ID: 2a9e143d8623
Revises: 
Create Date: 2022-11-05 23:01:56.771307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a9e143d8623'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    pass
