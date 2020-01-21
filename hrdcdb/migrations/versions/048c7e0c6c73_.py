"""empty message

Revision ID: 048c7e0c6c73
Revises: 6080b925ed30
Create Date: 2020-01-20 18:31:23.087476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '048c7e0c6c73'
down_revision = '6080b925ed30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_client_created_date'), 'client', ['created_date'], unique=False)
    op.add_column('client_address', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('client_address', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('client_address', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_client_address_created_date'), 'client_address', ['created_date'], unique=False)
    op.create_foreign_key(None, 'client_address', 'user', ['created_by'], ['id'])
    op.add_column('client_contact', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('client_contact', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('client_contact', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_client_contact_created_date'), 'client_contact', ['created_date'], unique=False)
    op.create_foreign_key(None, 'client_contact', 'user', ['created_by'], ['id'])
    op.add_column('client_race', sa.Column('created_by', sa.Integer(), nullable=True))
    op.add_column('client_race', sa.Column('created_date', sa.DateTime(), nullable=True))
    op.add_column('client_race', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_client_race_created_date'), 'client_race', ['created_date'], unique=False)
    op.create_foreign_key(None, 'client_race', 'user', ['created_by'], ['id'])
    op.create_index(op.f('ix_client_relationship_created_date'), 'client_relationship', ['created_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###