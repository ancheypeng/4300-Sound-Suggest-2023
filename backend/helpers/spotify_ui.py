import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sound_suggest_id = '0afed0e0b39e417f8c8603792a5c70c1'
sound_suggest_secret = 'ee3349373fde43939de5aa5a9b7f1273'

client_credentials_manager = SpotifyClientCredentials(client_id=sound_suggest_id, client_secret=sound_suggest_secret)
spotify_object = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def retrieve_spotify_data_for_frontend(query_song : str, query_artist: str):
    spotify_result_dict = dict()

    retrieved_results = spotify_object.search(q = "artist:" + query_artist + " track:" + query_song, limit = 1, type = "track")
    result_data = retrieved_results['tracks']['items'][0]

    song_title = result_data['name']

    song_url = result_data['external_urls']['spotify']

    cover_art_url = result_data['album']['images'][0]['url']

    artist_to_url_dict = dict()
    artists_array = result_data['artists'] 

    for artist in artists_array:
        artist_name = artist['name']
        artist_homepage = artist['external_urls']['spotify']
        artist_to_url_dict[artist_name] = artist_homepage

    spotify_result_dict['song_title'] = song_title
    spotify_result_dict['song_link'] = song_url
    spotify_result_dict['cover_art'] = cover_art_url
    spotify_result_dict['artists_links'] = artist_to_url_dict

    return spotify_result_dict



    