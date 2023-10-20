"""Initial Migration

Revision ID: a3ebea275cd2
Revises: 
Create Date: 2023-10-20 15:29:02.359423

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3ebea275cd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Colleges',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Courses',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('collegeid', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['collegeid'], ['Colleges.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Students',
    sa.Column('id', sa.String(length=10), nullable=False),
    sa.Column('firstname', sa.String(length=200), nullable=False),
    sa.Column('lastname', sa.String(length=200), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=200), nullable=False),
    sa.Column('courseid', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['courseid'], ['Courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('courses')
    op.drop_table('students')
    op.drop_table('colleges')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('colleges',
    sa.Column('id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('students',
    sa.Column('id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('firstname', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('lastname', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('year', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gender', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('courseid', mysql.VARCHAR(length=10), nullable=True),
    sa.ForeignKeyConstraint(['courseid'], ['courses.id'], name='students_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('courses',
    sa.Column('id', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('collegeid', mysql.VARCHAR(length=10), nullable=True),
    sa.ForeignKeyConstraint(['collegeid'], ['colleges.id'], name='courses_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('Students')
    op.drop_table('Courses')
    op.drop_table('Colleges')
    # ### end Alembic commands ###
