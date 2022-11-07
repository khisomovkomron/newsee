"""add column address_id to users table

Revision ID: 1fa6af05cb68
Revises: 06e521abbd9d
Create Date: 2022-11-07 22:42:46.691656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fa6af05cb68'
down_revision = '06e521abbd9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users', 'address_id')
