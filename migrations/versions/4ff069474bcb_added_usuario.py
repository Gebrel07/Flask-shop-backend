"""added usuario

Revision ID: 4ff069474bcb
Revises: 5aeca18bad6c
Create Date: 2023-11-07 19:23:38.135126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ff069474bcb'
down_revision = '5aeca18bad6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=300), nullable=False),
    sa.Column('email', sa.String(length=300), nullable=False),
    sa.Column('senha', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Usuario')
    # ### end Alembic commands ###
