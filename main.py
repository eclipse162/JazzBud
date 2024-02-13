import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os

def birdy_albums():
    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

def _30sec_samples():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.artist_top_tracks(lz_uri)

    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        print('audio    : ' + track['preview_url'])
        print('cover art: ' + track['album']['images'][0]['url'])
        print()

def get_artist_image():
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    if len(sys.argv) > 1:
        name = ' '.join(sys.argv[1:])
    else:
        name = 'Dave Brubeck'

    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        print(artist['name'], artist['images'][0]['url'])
def main():
    #birdy_albums()
    #_30sec_samples()
    #get_artist_image()

    # Authentication - without user, current not working
    #client_credentials_manager = SpotifyClientCredentials(client_id=os.environ['SPOTIFY_CLIENT_ID'], client_secret=os.environ['SPOTIFY_CLIENT_SECRET'])
    #sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    song_link = "https://open.spotify.com/track/1YQWosTIljIvxAgHWTp7KP"
    # parse song link
    s_uri = song_link.split("/")
    print(s_uri)
    song_uri = "1YQWosTIljIvxAgHWTp7KP"

    print(sp.audio_features(song_uri)[0])


main()