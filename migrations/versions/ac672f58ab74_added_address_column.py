"""added address column

Revision ID: ac672f58ab74
Revises: cf9e9a8184bf
Create Date: 2026-01-20 12:11:16.423789

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac672f58ab74'
down_revision = 'cf9e9a8184bf'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'user',
        sa.Column('address', sa.String(length=255), nullable=True)
    )

def downgrade():
    op.drop_column('user', 'address')
