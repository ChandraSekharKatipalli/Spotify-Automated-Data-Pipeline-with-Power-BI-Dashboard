import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def fetch_latest_albums():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
    albums = sp.new_releases(limit=10)['albums']['items']
    return pd.DataFrame([{
        'album_name': album['name'],
        'artist': album['artists'][0]['name'],
        'release_date': album['release_date']
    } for album in albums]).to_dict()


album_latest = fetch_latest_albums()

print(album_latest)