"""Add risk analytics fields to risks table

Revision ID: 002
Revises: 001
Create Date: 2026-01-18 17:24:32.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def column_exists(table_name, column_name):
    """Check if a column exists in a table."""
    conn = op.get_bind()
    result = conn.execute(text(
        f"SELECT column_name FROM information_schema.columns "
        f"WHERE table_name='{table_name}' AND column_name='{column_name}'"
    ))
    return result.fetchone() is not None


def table_exists(table_name):
    """Check if a table exists."""
    conn = op.get_bind()
    result = conn.execute(text(
        f"SELECT table_name FROM information_schema.tables "
        f"WHERE table_name='{table_name}'"
    ))
    return result.fetchone() is not None


def upgrade() -> None:
    # Add new columns to risks table only if they don't exist
    if not column_exists('risks', 'risk_score'):
        op.add_column('risks', sa.Column('risk_score', sa.Float(), nullable=True))
    
    if not column_exists('risks', 'trend'):
        op.add_column('risks', sa.Column('trend', sa.String(length=20), nullable=True, server_default='stable'))
    
    if not column_exists('risks', 'approval_status'):
        op.add_column('risks', sa.Column('approval_status', sa.String(length=50), nullable=True, server_default='pending'))
    
    if not column_exists('risks', 'approved_by'):
        op.add_column('risks', sa.Column('approved_by', sa.String(length=255), nullable=True))
    
    if not column_exists('risks', 'is_escalated'):
        op.add_column('risks', sa.Column('is_escalated', sa.Integer(), nullable=True, server_default='0'))
    
    # Create risk_metrics table only if it doesn't exist
    if not table_exists('risk_metrics'):
        op.create_table(
            'risk_metrics',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('risk_id', sa.Integer(), nullable=False),
            sa.Column('probability', sa.Integer(), nullable=False),
            sa.Column('impact', sa.Integer(), nullable=False),
            sa.Column('risk_score', sa.Float(), nullable=False),
            sa.Column('severity', sa.String(length=50), nullable=False),
            sa.Column('recorded_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.ForeignKeyConstraint(['risk_id'], ['risks.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_risk_metrics_recorded_at', 'risk_metrics', ['recorded_at'], unique=False)
        op.create_index('ix_risk_metrics_risk_id', 'risk_metrics', ['risk_id'], unique=False)


def downgrade() -> None:
    # Drop risk_metrics table if it exists
    if table_exists('risk_metrics'):
        op.drop_index('ix_risk_metrics_risk_id', table_name='risk_metrics')
        op.drop_index('ix_risk_metrics_recorded_at', table_name='risk_metrics')
        op.drop_table('risk_metrics')
    
    # Drop columns from risks table if they exist
    if column_exists('risks', 'is_escalated'):
        op.drop_column('risks', 'is_escalated')
    if column_exists('risks', 'approved_by'):
        op.drop_column('risks', 'approved_by')
    if column_exists('risks', 'approval_status'):
        op.drop_column('risks', 'approval_status')
    if column_exists('risks', 'trend'):
        op.drop_column('risks', 'trend')
    if column_exists('risks', 'risk_score'):
        op.drop_column('risks', 'risk_score')
