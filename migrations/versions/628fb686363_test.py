"""test

Revision ID: 628fb686363
Revises: None
Create Date: 2015-11-21 22:53:08.603475

"""

# revision identifiers, used by Alembic.
revision = '628fb686363'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test')
    ### end Alembic commands ###
