"""Add Notion integration table

Revision ID: b3f2a146f123
Revises: ca81bd47c050
Create Date: 2025-05-20 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b3f2a146f123'
down_revision = 'ca81bd47c050'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'notion_integration',
        sa.Column('project_id', sa.Text(), primary_key=True),
        sa.Column('database_id', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

def downgrade():
    op.drop_table('notion_integration')