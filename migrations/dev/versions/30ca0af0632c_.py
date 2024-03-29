"""empty message

Revision ID: 30ca0af0632c
Revises: 
Create Date: 2020-12-28 18:55:12.745480

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '30ca0af0632c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'league', ['uuid'])
    op.create_unique_constraint(None, 'status', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'status', type_='unique')
    op.drop_constraint(None, 'league', type_='unique')
    # ### end Alembic commands ###
