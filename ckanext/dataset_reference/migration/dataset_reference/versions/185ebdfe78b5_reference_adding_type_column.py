"""reference_adding_type_column

Revision ID: 185ebdfe78b5
Revises: da7a8c6c3926
Create Date: 2021-10-08 11:56:25.156062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '185ebdfe78b5'
down_revision = 'da7a8c6c3926'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('package_reference_link', sa.Column('adding_method', sa.UnicodeText, nullable=True))


def downgrade():
    pass
