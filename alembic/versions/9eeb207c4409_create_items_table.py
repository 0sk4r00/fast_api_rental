"""create items table

Revision ID: 9eeb207c4409
Revises: 
Create Date: 2023-03-26 14:33:21.667360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9eeb207c4409'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('items',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('items')
    pass
