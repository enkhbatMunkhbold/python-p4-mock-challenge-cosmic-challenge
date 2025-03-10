"""Add validations to models

Revision ID: 8d9e922d559d
Revises: ba918fdff388
Create Date: 2025-03-04 12:17:28.488410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d9e922d559d'
down_revision = 'ba918fdff388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('missions', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('missions', 'scientist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('missions', 'planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(op.f('fk_missions_scientist_id_scientists'), 'missions', 'scientists', ['scientist_id'], ['id'])
    op.create_foreign_key(op.f('fk_missions_planet_id_planets'), 'missions', 'planets', ['planet_id'], ['id'])
    op.alter_column('scientists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('scientists', 'field_of_study',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('scientists', 'field_of_study',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('scientists', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(op.f('fk_missions_planet_id_planets'), 'missions', type_='foreignkey')
    op.drop_constraint(op.f('fk_missions_scientist_id_scientists'), 'missions', type_='foreignkey')
    op.alter_column('missions', 'planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('missions', 'scientist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('missions', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
