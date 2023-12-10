"""added caract estoque imgs

Revision ID: 2d30d8f0593f
Revises: 4ff069474bcb
Create Date: 2023-11-23 16:04:44.493341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d30d8f0593f'
down_revision = '4ff069474bcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ProdutoCaract',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_produto', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descr', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['id_produto'], ['Produto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ProdutoEstoque',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_produto', sa.Integer(), nullable=False),
    sa.Column('variacao', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.Column('tamanho', sa.String(length=255), nullable=False),
    sa.Column('cor', sa.String(length=255), nullable=False),
    sa.Column('qtd', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['id_produto'], ['Produto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ProdutoImg',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_estoque', sa.Integer(), nullable=False),
    sa.Column('caminho', sa.String(length=255), nullable=False),
    sa.Column('ordem', sa.Integer(), server_default=sa.text('1'), nullable=False),
    sa.ForeignKeyConstraint(['id_estoque'], ['ProdutoEstoque.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Produto', schema=None) as batch_op:
        batch_op.drop_column('img')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Produto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.VARCHAR(length=255), nullable=True))

    op.drop_table('ProdutoImg')
    op.drop_table('ProdutoEstoque')
    op.drop_table('ProdutoCaract')
    # ### end Alembic commands ###
