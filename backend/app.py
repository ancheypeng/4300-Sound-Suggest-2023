import json
import os
from flask import Flask, render_template, request, send_file
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm

from helpers.spotify_ui import *

from sklearn.manifold import TSNE
import plotly.express as px

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "4300database"
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

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

with open('jsons/albums_to_lyric_svd_embeddings.json', 'r') as fp:
    albums_to_lyric_svd_embeddings = json.load(fp)

with open('jsons/albums_to_song_indexes.json', 'r') as fp:
    albums_to_song_indexes = json.load(fp)


tsne = TSNE(n_components=3, random_state=0, perplexity=20, learning_rate=15)


def cossim(a, b):
    return dot(a, b) / (norm(a) * norm(b))


@app.route("/")
def home():
    return render_template('base.html', title="Sound Suggest")


@app.route("/albums")
def get_albums():
    return list(album_to_songs_jaccard_truncated.keys())


@app.route("/tags")
def get_tags():
    return sorted(good_tags)


@app.route("/songs")
def songs_search():
    album = request.args.get("album")
    tags = set(request.args.getlist("tags"))

    album_lyric_vec = albums_to_lyric_svd_embeddings[album]
    album_song_indexes = set(albums_to_song_indexes[album])

    # stores tuples of (song idx, cossim score)
    cossim_scores = []

    for song_index, vec in enumerate(lyric_svd_embeddings):
        # ignore songs that are in the album
        if song_index in album_song_indexes:
            continue

        # print("cossim calculating...", song_index)
        score = cossim(album_lyric_vec, vec)

        song_tags = song_index_to_tags[str(song_index)] if str(
            song_index) in song_index_to_tags else []

        # increase score of songs that have matching tags
        for s in song_tags:
            song_tag = s[0]
            weight = s[1]
            if song_tag in tags:

                score *= 2 * (weight / 100)

                print("INCREASING SCORE OF", song_index,
                      "to", score)

        # increase score if artist matches
        album_artist = album.split(" - ")[1]
        song_artist = song_index_to_song_title_and_artist[str(
            song_index)]['artist']
        if album_artist == song_artist:
            score *= 1.2

        cossim_scores.append((song_index, score))

    cossim_scores = sorted(cossim_scores, reverse=True, key=lambda x: x[1])

    # print top scores for testing
    for i in range(10):
        print(cossim_scores[i])

    # song indexes sorted by cossim score
    top_songs = [js[0] for js in cossim_scores]

    # visualization_mat = []

    # for idx in albums_to_song_indexes[album]:
    #     visualization_mat.append(lyric_svd_embeddings[idx])

    # for idx in top_songs[:10]:
    #     visualization_mat.append(lyric_svd_embeddings[idx])

    # for i in range(len(top_songs)):
    #     if i % 200 == 0 and not i in top_songs[:10] and i not in albums_to_song_indexes[album]:
    #         visualization_mat.append(lyric_svd_embeddings[i])

    # visualization_mat = np.array(visualization_mat)
    # print(visualization_mat)
    # print(visualization_mat.shape)

    # print("running fit transform")
    # projections = tsne.fit_transform(visualization_mat)
    # print("fit transform done")

    # color = [2] * (len(albums_to_song_indexes[album])) + [1] * (10) + [0] * \
    #     (len(visualization_mat) - len(albums_to_song_indexes[album]) - 10)

    # fig = px.scatter_3d(
    #     projections, x=0, y=1, z=2,
    #     template="plotly_dark",
    #     color=color,
    #     opacity=0.7
    # )
    # fig.write_html("visualizations/projections.html")

    visualization_mat = []
    num_songs_in_album = len(album_song_indexes)

    for idx in album_song_indexes:
        visualization_mat.append(lyric_svd_embeddings[idx])

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
        if (data and not data in spotify_data):
            spotify_data.append(
                retrieve_spotify_data_for_frontend(title, artist))

            visualization_mat.append(lyric_svd_embeddings[idx])

        if (len(spotify_data) >= 10):
            break

    for i in range(len(top_songs)):
        if i % 200 == 0 and not i in top_songs[:10] and i not in album_song_indexes:
            visualization_mat.append(lyric_svd_embeddings[i])

    visualization_mat = np.array(visualization_mat)

    print("running fit transform")
    projections = tsne.fit_transform(visualization_mat)
    print("fit transform done")

    return_json = dict()

    return_json['album_song_names'] = [song_index_to_song_title_and_artist[str(
        song_index)]['title'] for song_index in album_song_indexes]
    return_json['album_song_embeddings'] = projections[:num_songs_in_album].tolist()
    return_json['suggested_song_embeddings'] = projections[num_songs_in_album: num_songs_in_album+10].tolist()
    return_json['random_song_embeddings'] = projections[num_songs_in_album+10:].tolist()

    return_json['spotify_data'] = list(spotify_data[:10])

    # return spotify data for up to 10 songs that had successful spotify queries
    return return_json


# app.run(debug=True)
