"""add repository_consent table

Revision ID: 64ae5a80f293
Revises: 0009
Create Date: 2026-10-07 16:29:55.814240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64ae5a80f293'
down_revision: Union[str, None] = '0009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'repository_consent',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('repository_type', sa.String(length=50), nullable=False),
        sa.Column('repository_url', sa.String(length=500), nullable=False),
        sa.Column('consent_given', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('consent_given_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('project_id', name='uq_repository_consent_project_id')
    )
    op.create_index('ix_repository_consent_project_id', 'repository_consent', ['project_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_repository_consent_project_id', table_name='repository_consent')
    op.drop_table('repository_consent')
