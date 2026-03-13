"""add address table

Revision ID: 98427cad27a0
Revises: 4b3b2b89f9fa
Create Date: 2026-01-20 12:58:29.577547

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '98427cad27a0'
down_revision = '4b3b2b89f9fa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'address',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('house_number', sa.String(length=50), nullable=True),
        sa.Column('street_name', sa.String(length=150), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('pincode', sa.String(length=20), nullable=False),
    )

def downgrade():
    op.drop_table('address')
