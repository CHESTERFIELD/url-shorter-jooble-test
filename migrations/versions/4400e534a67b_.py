"""empty message

Revision ID: 4400e534a67b
Revises: 
Create Date: 2021-02-04 18:00:28.262408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4400e534a67b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('full_url', sa.String(), nullable=False),
    sa.Column('url_hash', sa.String(), nullable=False),
    sa.Column('life_period', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('full_url'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('url_hash')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###
