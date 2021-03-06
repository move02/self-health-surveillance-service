"""empty message

Revision ID: dc4b5ab9d21f
Revises: bfb2b5fa8e7f
Create Date: 2020-08-24 17:13:22.572250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc4b5ab9d21f'
down_revision = 'bfb2b5fa8e7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_dummy',
    sa.Column('A', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('A'),
    mysql_collate='utf8_general_ci'
    )
    op.create_index(op.f('ix_t_dummy_A'), 't_dummy', ['A'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_t_dummy_A'), table_name='t_dummy')
    op.drop_table('t_dummy')
    # ### end Alembic commands ###
