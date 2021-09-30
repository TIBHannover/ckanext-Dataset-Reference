"""add_fields_for_proceedings

Revision ID: da7a8c6c3926
Revises: 20da9c08c5ec
Create Date: 2021-09-30 12:21:06.472700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da7a8c6c3926'
down_revision = '20da9c08c5ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('package_reference_link', sa.Column('conference_date', sa.UnicodeText, nullable=True))


def downgrade():
    pass
