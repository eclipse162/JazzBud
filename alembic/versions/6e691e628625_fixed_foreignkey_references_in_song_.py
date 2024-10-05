"""Fixed ForeignKey references in Song model

Revision ID: 6e691e628625
Revises: 75016a40b493
Create Date: 2024-10-05 01:25:05.658367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e691e628625'
down_revision: Union[str, None] = '75016a40b493'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('cover', sa.String(length=255), nullable=True))
    op.alter_column('artists', 'name',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)
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
    op.alter_column('artists', 'name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.drop_column('artists', 'cover')
    # ### end Alembic commands ###
