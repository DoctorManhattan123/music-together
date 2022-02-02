"""empty message

Revision ID: 0871929ae8ee
Revises: 
Create Date: 2022-02-02 01:43:26.496343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0871929ae8ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('music_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('music_room_uuid', sa.Text(), nullable=False),
    sa.Column('song_name', sa.Text(), nullable=False),
    sa.Column('content_url', sa.Text(), nullable=False),
    sa.Column('mp3_encoded', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('music_rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.Text(), nullable=False),
    sa.Column('music_room_name', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('secret', sa.Text(), nullable=False),
    sa.Column('salt', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('salt'),
    sa.UniqueConstraint('secret')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('music_rooms')
    op.drop_table('music_content')
    # ### end Alembic commands ###
