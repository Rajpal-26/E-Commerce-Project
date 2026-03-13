"""add images column to product table

Revision ID: 39f5a6691a5a
Revises: eb81cba6f09f
Create Date: 2026-01-23 11:13:38.749538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39f5a6691a5a'
down_revision = 'eb81cba6f09f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'product_details',
        sa.Column('images', sa.JSON(), nullable=True)
    )


def downgrade():
    op.drop_column('product_details', 'images')