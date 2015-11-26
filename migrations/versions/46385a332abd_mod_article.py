"""mod article

Revision ID: 46385a332abd
Revises: 4889e498fe37
Create Date: 2015-11-24 16:57:57.549999

"""

# revision identifiers, used by Alembic.
revision = '46385a332abd'
down_revision = '4889e498fe37'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('subject', sa.String(length=128), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'subject')
    ### end Alembic commands ###