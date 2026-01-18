"""add meeting fields

Revision ID: 004
Revises: 003
Create Date: 2026-01-18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to meetings table
    op.add_column('meetings', sa.Column('date', sa.Date(), nullable=True))
    op.add_column('meetings', sa.Column('time', sa.String(10), nullable=True))
    op.add_column('meetings', sa.Column('duration', sa.Integer(), nullable=True))
    op.add_column('meetings', sa.Column('attendees', JSON, nullable=True))
    op.add_column('meetings', sa.Column('status', sa.String(50), nullable=False, server_default='scheduled'))


def downgrade():
    # Remove columns
    op.drop_column('meetings', 'status')
    op.drop_column('meetings', 'attendees')
    op.drop_column('meetings', 'duration')
    op.drop_column('meetings', 'time')
    op.drop_column('meetings', 'date')
