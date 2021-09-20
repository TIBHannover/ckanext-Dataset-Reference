"""initialization

Revision ID: f5c00fdc4f95
Revises: 
Create Date: 2021-09-17 15:38:48.271609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5c00fdc4f95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'package_reference_link',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('package_name', sa.UnicodeText(), sa.ForeignKey('package.name'), nullable=False),
        sa.Column('doi', sa.UnicodeText(), nullable=False),        
        sa.Column('create_at', sa.DateTime(timezone=False), nullable=False),    
        sa.Column('citation', sa.UnicodeText, nullable=True)
    )


def downgrade():
    op.drop_table('package_reference_link')
