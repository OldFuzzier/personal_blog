"""empty message

Revision ID: a386baf08e65
Revises: 3ab00cc777ab
Create Date: 2017-12-11 00:26:16.368000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a386baf08e65'
down_revision = '3ab00cc777ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('role_id', table_name='user')
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_index('role_id', 'user', ['role_id'], unique=True)
    # ### end Alembic commands ###
