"""add_references_fields

Revision ID: 20da9c08c5ec
Revises: f5c00fdc4f95
Create Date: 2021-09-27 10:39:43.527915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20da9c08c5ec'
down_revision = 'f5c00fdc4f95'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('package_reference_link', sa.Column('authors', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('title', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('year', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('url', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('ref_type', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('publisher', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('place', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('journal', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('volume', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('issue', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('page', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('proceeding', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('access_date', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('organization', sa.UnicodeText, nullable=True))
    op.add_column('package_reference_link', sa.Column('thesis_type', sa.UnicodeText, nullable=True))


def downgrade():
    pass
