"""mod article

Revision ID: 46c42db38eb6
Revises: 46385a332abd
Create Date: 2015-11-24 16:59:46.068280

"""

# revision identifiers, used by Alembic.
revision = '46c42db38eb6'
down_revision = '46385a332abd'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('body', sa.UnicodeText(), nullable=False))
    op.drop_column('articles', 'details')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('details', mysql.TEXT(), nullable=False))
    op.drop_column('articles', 'body')
    ### end Alembic commands ###