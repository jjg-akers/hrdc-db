"""empty message

Revision ID: 0e29b59348fd
Revises: 53228e8b5ecc
Create Date: 2020-01-27 10:55:44.526820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e29b59348fd'
down_revision = '53228e8b5ecc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city_zip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=30), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    
    op.drop_table('client_address')
    op.create_table('client_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['zipcode'],['city_zip.zipcode'], ),
    sa.ForeignKeyConstraint(['created_by'],['user.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city_zip')

    op.drop_table('client_address')
    op.create_table('client_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('zipcode', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'],['user.id'], ),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
