"""add allocation optimizer

Revision ID: 003
Revises: 002
Create Date: 2026-01-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to projects table
    op.add_column('projects', sa.Column('priority', sa.Integer(), nullable=True, server_default='5'))
    op.add_column('projects', sa.Column('start_date', sa.DateTime(timezone=True), nullable=True))
    op.add_column('projects', sa.Column('deadline', sa.DateTime(timezone=True), nullable=True))
    
    # Add new columns to resources table
    op.add_column('resources', sa.Column('department', sa.String(100), nullable=True))
    op.add_column('resources', sa.Column('location', sa.String(100), nullable=True))
    
    # Create resource_skills table
    op.create_table(
        'resource_skills',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(100), nullable=False),
        sa.Column('proficiency_level', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_resource_skills_id', 'resource_skills', ['id'])
    op.create_index('ix_resource_skills_resource_id', 'resource_skills', ['resource_id'])
    op.create_index('ix_resource_skills_skill_name', 'resource_skills', ['skill_name'])
    
    # Create project_requirements table
    op.create_table(
        'project_requirements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(100), nullable=False),
        sa.Column('required_proficiency', sa.Integer(), nullable=False),
        sa.Column('required_hours', sa.Numeric(10, 2), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_project_requirements_id', 'project_requirements', ['id'])
    op.create_index('ix_project_requirements_project_id', 'project_requirements', ['project_id'])
    op.create_index('ix_project_requirements_skill_name', 'project_requirements', ['skill_name'])
    
    # Create allocation_scenarios table
    op.create_table(
        'allocation_scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('scenario_data', sa.JSON(), nullable=False),
        sa.Column('metrics', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_allocation_scenarios_id', 'allocation_scenarios', ['id'])


def downgrade() -> None:
    # Drop allocation_scenarios table
    op.drop_index('ix_allocation_scenarios_id', 'allocation_scenarios')
    op.drop_table('allocation_scenarios')
    
    # Drop project_requirements table
    op.drop_index('ix_project_requirements_skill_name', 'project_requirements')
    op.drop_index('ix_project_requirements_project_id', 'project_requirements')
    op.drop_index('ix_project_requirements_id', 'project_requirements')
    op.drop_table('project_requirements')
    
    # Drop resource_skills table
    op.drop_index('ix_resource_skills_skill_name', 'resource_skills')
    op.drop_index('ix_resource_skills_resource_id', 'resource_skills')
    op.drop_index('ix_resource_skills_id', 'resource_skills')
    op.drop_table('resource_skills')
    
    # Remove columns from resources table
    op.drop_column('resources', 'location')
    op.drop_column('resources', 'department')
    
    # Remove columns from projects table
    op.drop_column('projects', 'deadline')
    op.drop_column('projects', 'start_date')
    op.drop_column('projects', 'priority')
