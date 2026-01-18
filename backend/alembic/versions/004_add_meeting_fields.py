"""add meeting fields

Revision ID: 004
Revises: 003
Create Date: 2026-01-18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Get connection and inspector
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Get existing columns
    existing_columns = [col['name'] for col in inspector.get_columns('meetings')]
    
    # Add new columns only if they don't exist
    if 'date' not in existing_columns:
        op.add_column('meetings', sa.Column('date', sa.Date(), nullable=True))
    if 'time' not in existing_columns:
        op.add_column('meetings', sa.Column('time', sa.String(10), nullable=True))
    if 'duration' not in existing_columns:
        op.add_column('meetings', sa.Column('duration', sa.Integer(), nullable=True))
    if 'attendees' not in existing_columns:
        op.add_column('meetings', sa.Column('attendees', sa.Text(), nullable=True))
    if 'status' not in existing_columns:
        op.add_column('meetings', sa.Column('status', sa.String(50), nullable=True, server_default='scheduled'))


def downgrade():
    # Remove columns if they exist
    conn = op.get_bind()
    inspector = inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('meetings')]
    
    if 'status' in existing_columns:
        op.drop_column('meetings', 'status')
    if 'attendees' in existing_columns:
        op.drop_column('meetings', 'attendees')
    if 'duration' in existing_columns:
        op.drop_column('meetings', 'duration')
    if 'time' in existing_columns:
        op.drop_column('meetings', 'time')
    if 'date' in existing_columns:
        op.drop_column('meetings', 'date')
