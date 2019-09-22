"""Initial revision

Revision ID: 8e87452589a1
Revises:
Create Date: 2019-09-22 01:10:14.783562

"""
from alembic import op
import sqlalchemy as sa

from mautrix.bridge.db.mx_room_state import PowerLevelType


# revision identifiers, used by Alembic.
revision = '8e87452589a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('mxid', sa.String(length=255), nullable=True),
    sa.Column('mx_room', sa.String(length=255), nullable=True),
    sa.Column('tw_receiver', sa.String(length=127), nullable=False),
    sa.Column('twid', sa.String(length=127), nullable=False),
    sa.PrimaryKeyConstraint('tw_receiver', 'twid')
    )
    op.create_table('mx_room_state',
    sa.Column('room_id', sa.String(length=255), nullable=False),
    sa.Column('power_levels', PowerLevelType(), nullable=True),
    sa.PrimaryKeyConstraint('room_id')
    )
    op.create_table('mx_user_profile',
    sa.Column('room_id', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('membership', sa.Enum('JOIN', 'LEAVE', 'INVITE', 'BAN', 'KNOCK', name='membership'), nullable=False),
    sa.Column('displayname', sa.String(), nullable=True),
    sa.Column('avatar_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('room_id', 'user_id')
    )
    op.create_table('portal',
    sa.Column('twid', sa.String(length=127), nullable=False),
    sa.Column('mxid', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('twid')
    )
    op.create_table('puppet',
    sa.Column('twid', sa.String(length=127), nullable=False),
    sa.Column('matrix_registered', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    sa.PrimaryKeyConstraint('twid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('puppet')
    op.drop_table('portal')
    op.drop_table('mx_user_profile')
    op.drop_table('mx_room_state')
    op.drop_table('message')
    # ### end Alembic commands ###
