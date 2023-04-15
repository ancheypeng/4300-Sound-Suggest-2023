import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

sound_suggest_id = '0afed0e0b39e417f8c8603792a5c70c1'
sound_suggest_secret = 'ee3349373fde43939de5aa5a9b7f1273'

client_credentials_manager = SpotifyClientCredentials(client_id=sound_suggest_id, client_secret=sound_suggest_secret)
spotify_object = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def retrieve_spotify_data_for_frontend(query_song : str, query_artist: str):
    retrieved_results = spotify_object.search(q = "artist:" + query_artist + " track:" + query_artist, limit = 1, type = "track")
    