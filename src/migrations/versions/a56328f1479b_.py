"""empty message

Revision ID: a56328f1479b
Revises: 85283bba0420
Create Date: 2016-01-26 10:30:08.365700

"""

# revision identifiers, used by Alembic.
revision = 'a56328f1479b'
down_revision = '85283bba0420'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('domain_id_account_uc', 'account', ['domain_id', 'account_name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('domain_id_account_uc', 'account', type_='unique')
    ### end Alembic commands ###
