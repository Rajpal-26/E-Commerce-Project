"""create user table

Revision ID: 76db806be9ca
Revises: 0e4346ffbf60
Create Date: 2026-01-13 12:01:50.584911

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '76db806be9ca'
down_revision = '0e4346ffbf60'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False)
    )


def downgrade():
    op.drop_table('user')

