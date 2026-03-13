"""add cart and cartItem table

Revision ID: 102d043ab790
Revises: 39f5a6691a5a
Create Date: 2026-01-28 11:28:45.272210

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '102d043ab790'
down_revision = '39f5a6691a5a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cart',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cart_id', sa.Integer(), sa.ForeignKey('cart.id'), nullable=False),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product_details.id'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default="1"),
        sa.Column('price_at_time', sa.Float(), nullable=False),
        sa.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
    )

def downgrade():
    op.drop_table('cart_items')
    op.drop_table('cart')