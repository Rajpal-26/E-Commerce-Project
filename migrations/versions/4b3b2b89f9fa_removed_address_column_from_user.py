"""removed address column from user

Revision ID: 4b3b2b89f9fa
Revises: ac672f58ab74
Create Date: 2026-01-20 12:30:59.911431

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4b3b2b89f9fa'
down_revision = 'ac672f58ab74'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("user", "address")

def downgrade():
    op.add_column(
        "user",
        sa.Column("address", sa.String(length=255), nullable=True)
    )
