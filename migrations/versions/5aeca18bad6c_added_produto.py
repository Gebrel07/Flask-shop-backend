"""added produto

Revision ID: 5aeca18bad6c
Revises: 
Create Date: 2023-11-06 14:57:27.935360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5aeca18bad6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Produto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=400), nullable=False),
    sa.Column('descricao', sa.String(length=500), nullable=True),
    sa.Column('preco', sa.Float(precision=2), server_default=sa.text('0'), nullable=False),
    sa.Column('img', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Produto')
    # ### end Alembic commands ###