"""finish him

Revision ID: 4d4d4dc13ca3
Revises: 9e26db5c7adc
Create Date: 2019-11-02 15:25:10.201876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d4d4dc13ca3'
down_revision = '9e26db5c7adc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('read', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification', 'read')
    # ### end Alembic commands ###