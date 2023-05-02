import json
import os
from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import editdistance

from helpers.spotify_ui import *

from sklearn.manifold import TSNE

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# # These are the DB credentials for your OWN MySQL
# # Don't worry about the deployment credentials, those are fixed
# # You can use a different DB name if you want to
# MYSQL_USER = "root"
# MYSQL_USER_PASSWORD = "4300database"
# MYSQL_PORT = 3306
# MYSQL_DATABASE = "kardashiandb"

# mysql_engine = MySQLDatabaseHandler(
#     MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# # # Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
# mysql_engine.load_file_into_db()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)


with open('jsons/album_to_songs_jaccard_truncated.json', 'r') as fp:
    album_to_songs_jaccard_truncated = json.load(fp)

with open('jsons/song_index_to_song_title_and_artist.json', 'r') as fp:
    song_index_to_song_title_and_artist = json.load(fp)

with open('jsons/song_index_to_tags.json', 'r') as fp:
    song_index_to_tags = json.load(fp)

with open('jsons/good_tags.json', 'r') as fp:
    good_tags = json.load(fp)

with open('jsons/lyric_svd_embeddings.json', 'r') as fp:
    lyric_svd_embeddings = json.load(fp)

with open('jsons/tag_svd_embeddings.json', 'r') as fp:
    tag_svd_embeddings = json.load(fp)

with open('jsons/albums_to_lyric_svd_embeddings.json', 'r') as fp:
    albums_to_lyric_svd_embeddings = json.load(fp)

with open('jsons/albums_to_tag_svd_embeddings.json', 'r') as fp:
    albums_to_tag_svd_embeddings = json.load(fp)

with open('jsons/albums_to_song_indexes.json', 'r') as fp:
    albums_to_song_indexes = json.load(fp)

with open('jsons/named_tags.json', 'r') as fp:
    named_tags = json.load(fp)

# best: perplexity=20, learning_rate=15
tsne = TSNE(n_components=3, random_state=0,
            perplexity=20, learning_rate=20)


def cossim(a, b):
    ans = dot(a, b) / (norm(a) * norm(b))
    if not ans or pd.isna(ans):
        return 0
    return ans


@app.route("/")
def home():
    return render_template('base.html', title="Sound Suggest")


@app.route("/albums")
def get_albums():
    return list(album_to_songs_jaccard_truncated.keys())


@app.route("/tags")
def get_tags():
    return sorted(good_tags)


def normalize_score(score):
    if score > 0.95:
        score = score / (score + 0.05)

    return round(score, 4) * 100


@app.route("/songs")
def songs_search():
    album = request.args.get("album")
    tags = set(request.args.getlist("tags"))

    sameArtist = request.args.getlist("sameArtist")[0] == 'on'

    album_lyric_vec = albums_to_lyric_svd_embeddings[album]
    album_tag_vec = albums_to_tag_svd_embeddings[album]
    album_song_indexes = set(albums_to_song_indexes[album])

    # stores tuples of (song idx, cossim score)
    cossim_scores = dict()

    for song_index, (song_lyric_vec, song_tag_vec) in enumerate(zip(lyric_svd_embeddings, tag_svd_embeddings)):
        # ignore songs that are in the album
        if song_index in album_song_indexes:
            continue

        score = 0

        # if tag vector is 0, use only lyric vector
        if (sum(song_tag_vec) == 0 or sum(album_lyric_vec) == 0):
            score = cossim(album_lyric_vec, song_lyric_vec)
        # else use weighted sum of lyric cossim and tag cossim
        else:
            score = 0.6 * cossim(album_lyric_vec, song_lyric_vec) + \
                0.4 * cossim(album_tag_vec, song_tag_vec)

        song_tags = song_index_to_tags[str(song_index)] if str(
            song_index) in song_index_to_tags else []

        # increase score of songs that have matching tags
        for s in song_tags:
            song_tag = s[0]
            weight = int(s[1])
            if song_tag in tags:

                score *= 3 * (weight / 100)

                print("INCREASING SCORE OF", song_index,
                      "to", score)

        # increase score if artist matches
        album_artist = album.split(" - ")[1]
        song_artist = song_index_to_song_title_and_artist[str(
            song_index)]['artist']
        if album_artist == song_artist:
            if sameArtist:
                score *= 1.1
            else:
                score = 0

        cossim_scores[song_index] = score

    sorted_scores = sorted(cossim_scores.items(),
                           reverse=True, key=lambda x: x[1])

    # print top scores for testing
    for i in range(10):
        print(sorted_scores[i])

    # song indexes sorted by cossim score
    top_songs = [js[0] for js in sorted_scores]

    tsne_mat = [album_lyric_vec]
    num_songs_in_album = len(album_song_indexes)

    album_radial_vec = [album_tag_vec[idx]
                        for idx in named_tags.values()]
    album_radial_vec.append(album_radial_vec[0])
    radial_mat = [album_radial_vec]

    for idx in album_song_indexes:
        tsne_mat.append(lyric_svd_embeddings[idx])

    # get song and artist from the indexes
    songs = [song_index_to_song_title_and_artist[str(
        song_index)] for song_index in top_songs]

    # get spotify data for the songs
    spotify_data = []

    for song_index, song in zip(top_songs, songs):
        title = song['title']
        artist = song['artist']
        data = retrieve_spotify_data_for_frontend(title, artist)

        # check that spotify data exists and not a repeat
        if (not data or data in spotify_data):
            continue

        spotify_artists = data['artists']

        # check if artist matches using edit distance

        matching_artist = False

        for spotify_artist in spotify_artists:
            edit_distance = editdistance.eval(artist, spotify_artist['name'])
            matching_artist = matching_artist or edit_distance / \
                len(artist) < 0.5

        if not matching_artist:
            print('no matching artist')
            continue

        data['score'] = normalize_score(cossim_scores[song_index])

        spotify_data.append(data)

        tsne_mat.append(lyric_svd_embeddings[song_index])

        named_tag_vec = [tag_svd_embeddings[song_index][idx]
                         for idx in named_tags.values()]

        named_tag_vec.append(named_tag_vec[0])

        radial_mat.append(named_tag_vec)

        if (len(spotify_data) >= 10):
            break

    for i in range(len(top_songs)):
        if i % 300 == 0 and not i in top_songs[:10] and i not in album_song_indexes:
            tsne_mat.append(lyric_svd_embeddings[i])

    tsne_mat = np.array(tsne_mat)

    print("running fit transform")
    projections = tsne.fit_transform(tsne_mat).tolist()
    print("fit transform done")

    return_json = dict()

    return_json['album_song_names'] = [song_index_to_song_title_and_artist[str(
        song_index)]['title'] for song_index in album_song_indexes]

    return_json['album_centroid'] = projections.pop(0)
    return_json['album_song_embeddings'] = projections[:num_songs_in_album]
    return_json['suggested_song_embeddings'] = projections[
        num_songs_in_album: num_songs_in_album+10]
    return_json['random_song_embeddings'] = projections[
        num_songs_in_album+10:]

    return_json['radial_dimensions'] = list(
        named_tags.keys()) + [list(named_tags.keys())[0]]
    return_json['radial_data'] = radial_mat
    # print(radial_mat)

    return_json['spotify_data'] = list(spotify_data[:10])

    # return spotify data for up to 10 songs that had successful spotify queries
    return return_json


# app.run(debug=True)
