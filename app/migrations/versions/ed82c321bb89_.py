"""empty message

Revision ID: ed82c321bb89
Revises: c8e955c47211
Create Date: 2023-04-17 14:28:06.376914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed82c321bb89'
down_revision = 'c8e955c47211'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prize',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('can_collect', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prize')
    # ### end Alembic commands ###