"""create order and order_items table

Revision ID: c7cfc2a61b96
Revises: 102d043ab790
Create Date: 2026-01-29 15:39:01.425385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c7cfc2a61b96'
down_revision = '102d043ab790'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Create orders
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('total_price', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now())
    )

    # 2. Create order_items
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('product_details.id')),
        sa.Column('quantity', sa.Integer, nullable=False),
    )

    # 3. Fix cart_items safely
    with op.batch_alter_table('cart_items') as batch_op:
        # Only drop FK if it exists
        batch_op.execute("""
        SET @fk := (
            SELECT CONSTRAINT_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'cart_items'
            AND CONSTRAINT_SCHEMA = DATABASE()
            AND REFERENCED_TABLE_NAME IS NOT NULL
            LIMIT 1
        );
        """)