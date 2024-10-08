"""Change User field name type to userType

Revision ID: ac3d6be74091
Revises: 1153df717c9b
Create Date: 2024-09-02 16:57:22.845990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac3d6be74091'
down_revision = '1153df717c9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userType', sa.Integer(), nullable=False))
        batch_op.drop_column('type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.INTEGER(), nullable=False))
        batch_op.drop_column('userType')

    # ### end Alembic commands ###
