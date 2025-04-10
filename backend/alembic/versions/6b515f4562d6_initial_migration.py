"""initial migration

Revision ID: 6b515f4562d6
Revises: 
Create Date: 2025-03-16 21:45:48.271500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b515f4562d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('artist_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sp_artist_id', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('cover', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('artist_id'),
    sa.UniqueConstraint('sp_artist_id')
    )
    op.create_index(op.f('ix_artists_name'), 'artists', ['name'], unique=False)
    op.create_table('instruments',
    sa.Column('instrument_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('instrument_id')
    )
    op.create_index(op.f('ix_instruments_name'), 'instruments', ['name'], unique=True)
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('session_id', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('spotify_user_id', sa.String(length=255), nullable=True),
    sa.Column('is_authenticated', sa.Boolean(), nullable=True),
    sa.Column('display_name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('spotify_user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('albums',
    sa.Column('album_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sp_album_id', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('cover', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('album_id'),
    sa.UniqueConstraint('sp_album_id')
    )
    op.create_index(op.f('ix_albums_name'), 'albums', ['name'], unique=False)
    op.create_table('tokens',
    sa.Column('token_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('access_token', sa.String(length=500), nullable=True),
    sa.Column('refresh_token', sa.String(length=500), nullable=True),
    sa.Column('expires_in', sa.DateTime(), nullable=True),
    sa.Column('token_type', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.create_table('songs',
    sa.Column('song_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('spotify_song_id', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('release_year', sa.Integer(), nullable=True),
    sa.Column('track_length', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['albums.album_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('song_id'),
    sa.UniqueConstraint('spotify_song_id')
    )
    op.create_index(op.f('ix_songs_title'), 'songs', ['title'], unique=False)
    op.create_table('collections',
    sa.Column('collection_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('song_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('collection_name', sa.String(length=50), nullable=False),
    sa.Column('collection_description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['song_id'], ['songs.song_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('collection_id')
    )
    op.create_table('sections',
    sa.Column('section_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('section_name', sa.String(length=50), nullable=False),
    sa.Column('start_time', sa.Integer(), nullable=False),
    sa.Column('end_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.collection_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('section_id')
    )
    op.create_index(op.f('ix_sections_section_name'), 'sections', ['section_name'], unique=False)
    op.create_table('segments',
    sa.Column('segment_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('segment_name', sa.String(length=50), nullable=False),
    sa.Column('start_time', sa.Integer(), nullable=False),
    sa.Column('end_time', sa.Integer(), nullable=False),
    sa.Column('segment_description', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['collections.collection_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('segment_id')
    )
    op.create_index(op.f('ix_segments_segment_name'), 'segments', ['segment_name'], unique=False)
    op.create_table('segment_artists',
    sa.Column('segment_id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.artist_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['instrument_id'], ['instruments.instrument_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['segment_id'], ['segments.segment_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('segment_id', 'artist_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('segment_artists')
    op.drop_index(op.f('ix_segments_segment_name'), table_name='segments')
    op.drop_table('segments')
    op.drop_index(op.f('ix_sections_section_name'), table_name='sections')
    op.drop_table('sections')
    op.drop_table('collections')
    op.drop_index(op.f('ix_songs_title'), table_name='songs')
    op.drop_table('songs')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_albums_name'), table_name='albums')
    op.drop_table('albums')
    op.drop_table('users')
    op.drop_index(op.f('ix_instruments_name'), table_name='instruments')
    op.drop_table('instruments')
    op.drop_index(op.f('ix_artists_name'), table_name='artists')
    op.drop_table('artists')
    # ### end Alembic commands ###
