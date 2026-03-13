"""add created at column to address table

Revision ID: eb81cba6f09f
Revises: 98427cad27a0
Create Date: 2026-01-22 11:06:41.923758

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eb81cba6f09f'
down_revision = '98427cad27a0'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add column as nullable
    op.add_column(
        'address',
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 2. Fill existing rows
    op.execute(
        "UPDATE address SET created_at = UTC_TIMESTAMP() WHERE created_at IS NULL"
    )

    # 3. Make it NOT NULL (MySQL requires existing_type)
    op.alter_column(
        'address',
        'created_at',
        existing_type=sa.DateTime(timezone=True),
        nullable=False
    )


def downgrade():
    op.drop_column('address', 'created_at')
