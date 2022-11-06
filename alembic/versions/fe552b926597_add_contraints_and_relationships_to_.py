"""add contraints and relationships to User and Todo tables

Revision ID: fe552b926597
Revises: 2a9e143d8623
Create Date: 2022-11-07 00:28:50.122859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe552b926597'
down_revision = '2a9e143d8623'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('todos', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key('todo_users_fk', source_table='todos', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('todo_users_fk', table_name='todos')
    op.drop_column('todos', 'owner_id')
