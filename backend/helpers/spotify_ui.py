import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sound_suggest_id = '0afed0e0b39e417f8c8603792a5c70c1'
sound_suggest_secret = 'ee3349373fde43939de5aa5a9b7f1273'

client_credentials_manager = SpotifyClientCredentials(
    client_id=sound_suggest_id, client_secret=sound_suggest_secret)
spotify_object = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def retrieve_spotify_data_for_frontend(query_song: str, query_artist: str):
    spotify_result_dict = dict()
    # print(query_song, query_artist)
    retrieved_results = spotify_object.search(
        q="artist:" + query_artist + " track:" + query_song, limit=1, market = "US", type="track")

    if not retrieved_results['tracks']['items']:
        return None

    result_data = retrieved_results['tracks']['items'][0]

    song_title = result_data['name']

    song_url = result_data['external_urls']['spotify']

    preview_url = result_data['preview_url']

    cover_art_url = result_data['album']['images'][0]['url']

    artist_dict_list = []
    artists_array = result_data['artists']

    for artist in artists_array:
        artist_name = artist['name']
        artist_homepage = artist['external_urls']['spotify']
        artist_dict = dict()
        artist_dict["name"] = artist_name
        artist_dict["link"] = artist_homepage

        artist_dict_list.append(artist_dict)

    spotify_result_dict['song'] = song_title
    spotify_result_dict['link'] = song_url
    spotify_result_dict['thumbnail'] = cover_art_url
    spotify_result_dict['artists'] = artist_dict_list
    spotify_result_dict['preview'] = preview_url

    return spotify_result_dict
