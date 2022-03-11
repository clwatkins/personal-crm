"""Create User table

Revision ID: c16bb4dcc300
Revises: 
Create Date: 2022-03-06 13:54:28.368744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func
import datetime as dt


# revision identifiers, used by Alembic.
revision = 'c16bb4dcc300'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('created_at', sa.DATETIME(), nullable=False, server_default=func.now()))


def downgrade():
    op.drop_table('users')
