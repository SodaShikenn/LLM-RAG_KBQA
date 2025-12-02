"""baseline initial schema

Revision ID: baseline
Revises:
Create Date: 2025-11-17 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'baseline'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # This is a baseline migration - all tables already exist in the database
    # No changes needed
    pass


def downgrade():
    # Cannot downgrade from baseline
    pass
