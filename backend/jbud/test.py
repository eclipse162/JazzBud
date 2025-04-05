import spotipy
import pprint

from spotipy.oauth2 import SpotifyOAuth


def format_song_details(sp, song_url):
    """
    sp = Spotify Manager
    song_url = Song URL to be parsed

    Returns:
        Dict object with the following metadata extracted from the song URL:
            - spotify_song_id, title, artist, album, genre, release_year
    """
    results = sp.track(song_url)
    song_dict = dict()


    song_dict["spotify_song_id"] = results["id"]
    song_dict["title"] = results["name"]
    song_dict["artist"] = results["artists"][0]["name"]
    song_dict["album"] = results["album"]["name"]
    song_dict["genre"] = sp.artist(results["artists"][0]["id"])["genres"][0]
    song_dict["release_year"] = results["album"]["release_date"].split("-")[0]

    return song_dict


def main():

    c_id = "0fc60274694a45318c2bae2dd7e9584a"
    c_secret = "7facc5e90f7b411f90b45d2e8a6d7498"
    uri = "https://open.spotify.com"
    track_query = "https://open.spotify.com/track/0QZKaC3N3DRl0E5M497Nde?si=6c24fe854e3a491c"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=c_id,
                                                   client_secret=c_secret,
                                                   redirect_uri=uri,
                                                   scope="user-library-read"))


    song_details = format_song_details(sp, track_query)

    pprint.pprint(song_details)


main()