"""removed unique field from name

Revision ID: 0e4346ffbf60
Revises: a910b831398a
Create Date: 2026-01-07 18:35:51.176692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e4346ffbf60'
down_revision = 'a910b831398a'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_constraint(
    #     'product_details_name_key',  # 👈 replace with actual Key_name
    #     'product_details',
    #     type_='unique'
    # )
    # op.drop_index('product_details_name_unique', table_name='product_details')
    pass

def downgrade():
    op.create_unique_constraint(
        'product_details_name_key',
        'product_details',
        ['name']
    )
    with op.batch_alter_table('product_details', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('name'), ['name'], unique=True)
        batch_op.create_index(batch_op.f('model_number'), ['model_number'], unique=True)

    op.drop_table('Product_Details')
    # ### end Alembic commands ###
