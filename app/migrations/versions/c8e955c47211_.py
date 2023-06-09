"""empty message

Revision ID: c8e955c47211
Revises: 
Create Date: 2023-04-17 14:24:44.204662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8e955c47211'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chatId', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('economistissue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('month', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('newquest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('answer_count', sa.Integer(), nullable=True),
    sa.Column('correct_answer', sa.Integer(), nullable=True),
    sa.Column('answers', sa.PickleType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('newquiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('quest_count', sa.Integer(), nullable=True),
    sa.Column('filled_quest', sa.Integer(), nullable=True),
    sa.Column('reward', sa.Boolean(), nullable=True),
    sa.Column('reward_type', sa.String(), nullable=True),
    sa.Column('rewards', sa.PickleType(), nullable=True),
    sa.Column('rewards_remain', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('quest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('answer_count', sa.Integer(), nullable=True),
    sa.Column('correct_answer', sa.Integer(), nullable=True),
    sa.Column('answers', sa.PickleType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quiz',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('quest_count', sa.Integer(), nullable=True),
    sa.Column('reward', sa.Boolean(), nullable=True),
    sa.Column('reward_type', sa.String(), nullable=True),
    sa.Column('rewards', sa.PickleType(), nullable=True),
    sa.Column('rewards_remain', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('rewards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('can_collect', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chatId', sa.BigInteger(), nullable=False),
    sa.Column('sub_status', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('quiz_current', sa.Integer(), nullable=True),
    sa.Column('gpt_context', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('rewards')
    op.drop_table('quiz')
    op.drop_table('quest')
    op.drop_table('newquiz')
    op.drop_table('newquest')
    op.drop_table('economistissue')
    op.drop_table('admin')
    # ### end Alembic commands ###
