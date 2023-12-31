"""empty message

Revision ID: 2116e78293d1
Revises: 
Create Date: 2023-06-26 10:45:39.411502

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2116e78293d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('img', sa.String(length=200), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('url', sa.String(length=300), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('icon', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=320), nullable=False),
    sa.Column('avatar', sa.String(length=200), nullable=True),
    sa.Column('gexing', sa.String(length=100), nullable=True),
    sa.Column('desc', sa.String(length=150), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=150), nullable=True),
    sa.Column('is_super_user', sa.Boolean(), nullable=True),
    sa.Column('is_first_user', sa.Boolean(), nullable=True),
    sa.Column('is_second_user', sa.Boolean(), nullable=True),
    sa.Column('is_third_user', sa.Boolean(), nullable=True),
    sa.Column('is_fourth_user', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_staff', sa.Boolean(), nullable=True),
    sa.Column('inspect', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('inspect_post',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('content', mysql.LONGTEXT(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_inspect', sa.Boolean(), nullable=True),
    sa.Column('is_pass', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('content', mysql.LONGTEXT(), nullable=False),
    sa.Column('has_type', sa.Enum('draft', 'show', name='postpublishtype'), server_default='show', nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('add_date', sa.DateTime(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('tag_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('inspect_post')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('category')
    op.drop_table('banner')
    # ### end Alembic commands ###
