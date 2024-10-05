"""Fixed ForeignKey references in Song model

Revision ID: 3494eb466e37
Revises: 75016a40b493
Create Date: 2024-10-05 01:16:33.680960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75016a40b493'
down_revision = '0b923ca42da9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('sp_artist_id', sa.String(length=255), nullable=True))
    op.alter_column('artists', 'artist_id',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               nullable=False,
               autoincrement=True)
    op.drop_column('artists', 'id')
    op.drop_column('artists', 'slug')
    op.add_column('songs', sa.Column('sp_song_id', sa.String(length=255), nullable=True))
    op.alter_column('songs', 'artist_id',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               nullable=False)
    op.alter_column('songs', 'album_id',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.Integer(),
               nullable=False)
    op.create_foreign_key(None, 'songs', 'albums', ['album_id'], ['album_id'])
    op.create_foreign_key(None, 'songs', 'artists', ['artist_id'], ['artist_id'])
    op.drop_column('songs', 'spotify_song_id')
    op.drop_column('songs', 'artist_slug')
    op.drop_column('songs', 'album_slug')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songs', sa.Column('album_slug', sa.VARCHAR(length=255), nullable=False))
    op.add_column('songs', sa.Column('artist_slug', sa.VARCHAR(length=255), nullable=False))
    op.add_column('songs', sa.Column('spotify_song_id', sa.VARCHAR(length=255), nullable=True))
    op.drop_constraint(None, 'songs', type_='foreignkey')
    op.drop_constraint(None, 'songs', type_='foreignkey')
    op.alter_column('songs', 'album_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('songs', 'artist_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('songs', 'sp_song_id')
    op.add_column('artists', sa.Column('slug', sa.VARCHAR(length=255), nullable=False))
    op.add_column('artists', sa.Column('id', sa.INTEGER(), nullable=False))
    op.alter_column('artists', 'artist_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=255),
               nullable=True,
               autoincrement=True)
    op.drop_column('artists', 'sp_artist_id')
    # ### end Alembic commands ###
