"""empty message

Revision ID: 354a3f5de305
Revises: b1a57da9eccf
Create Date: 2022-03-07 20:39:57.616781

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '354a3f5de305'
down_revision = 'b1a57da9eccf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('usuario_ibfk_2', 'usuario', type_='foreignkey')
    op.drop_constraint('usuario_ibfk_1', 'usuario', type_='foreignkey')
    op.drop_column('usuario', 'personaje_id')
    op.drop_column('usuario', 'planeta_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('planeta_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('usuario', sa.Column('personaje_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('usuario_ibfk_1', 'usuario', 'personaje', ['personaje_id'], ['id'])
    op.create_foreign_key('usuario_ibfk_2', 'usuario', 'planeta', ['planeta_id'], ['id'])
    # ### end Alembic commands ###
