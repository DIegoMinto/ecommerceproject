"""Adición de productos categorias 1-5

Revision ID: c951044a3108
Revises: 80a2010bbd6d
Create Date: 2024-09-19 09:22:37.411687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c951044a3108'
down_revision = '80a2010bbd6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_column('description')

    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.alter_column('descripcion',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.Text(),
               existing_nullable=True)
        batch_op.alter_column('imagen_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('marca',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('especificaciones',
               existing_type=sa.VARCHAR(length=1000),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.alter_column('especificaciones',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=1000),
               existing_nullable=True)
        batch_op.alter_column('marca',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('imagen_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('descripcion',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)

    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=200), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
