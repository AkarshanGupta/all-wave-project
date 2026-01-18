"""Add risk analytics fields to risks table

Revision ID: 002_add_risk_analytics
Revises: 001_initial_migration
Create Date: 2026-01-18 17:24:32.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_risk_analytics'
down_revision = '001_initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to risks table
    op.add_column('risks', sa.Column('risk_score', sa.Float(), nullable=True))
    op.add_column('risks', sa.Column('trend', sa.String(length=20), server_default='stable'))
    op.add_column('risks', sa.Column('approval_status', sa.String(length=50), server_default='pending'))
    op.add_column('risks', sa.Column('approved_by', sa.String(length=255), nullable=True))
    op.add_column('risks', sa.Column('is_escalated', sa.Integer(), server_default='0'))
    
    # Create risk_metrics table
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
    op.create_index(op.f('ix_risk_metrics_recorded_at'), 'risk_metrics', ['recorded_at'], unique=False)
    op.create_index(op.f('ix_risk_metrics_risk_id'), 'risk_metrics', ['risk_id'], unique=False)


def downgrade() -> None:
    # Drop risk_metrics table
    op.drop_index(op.f('ix_risk_metrics_risk_id'), table_name='risk_metrics')
    op.drop_index(op.f('ix_risk_metrics_recorded_at'), table_name='risk_metrics')
    op.drop_table('risk_metrics')
    
    # Drop columns from risks table
    op.drop_column('risks', 'is_escalated')
    op.drop_column('risks', 'approved_by')
    op.drop_column('risks', 'approval_status')
    op.drop_column('risks', 'trend')
    op.drop_column('risks', 'risk_score')
