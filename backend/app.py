import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd
import numpy as np

from helpers.spotify_ui import *

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "R9sU85ujC"
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this

with open('jsons/album_to_songs_jaccard_truncated.json', 'r') as fp:
    album_to_songs_jaccard_truncated = json.load(fp)

with open('jsons/song_index_to_song_title_and_artist.json', 'r') as fp:
    song_index_to_song_title_and_artist = json.load(fp)

with open('jsons/song_index_to_tags.json', 'r') as fp:
    song_index_to_tags = json.load(fp)

with open('jsons/good_tags.json', 'r') as fp:
    good_tags = json.load(fp)


def sql_search(episode):
    # query_sql = f"""SELECT * FROM mytable WHERE LOWER( Album ) LIKE '%%{episode.lower()}%%' limit 10"""
    # keys = ["Artist", "Title", "Album", "Year", "Date", "Lyric", "Genre"]
    # data = mysql_engine.query_selector(query_sql)
    # return json.dumps([dict(zip(keys, i)) for i in data])
    df = pd.read_csv('jaccard1.csv')
    query = episode.lower()
    # creates new dataframe of only rows of songs inside album specified by query
    tmp = df.loc[df['Unnamed: 0'].str.lower() == query]
    size = len(tmp)
    tmpSum = tmp.sum(numeric_only=True, axis=0)  # gets sum of all columns
    tmpAvg = tmpSum.divide(size)  # gets avg of all columns
    tmpAns = tmpAvg.to_numpy()
    songs = df.columns.tolist()[1::]
    tples = zip(tmpAns, songs)  # tple list (jac val, song name)
    tples = sorted(tples, reverse=True)
    ans = [song for (_, song) in tples[0:10]]  # list of only top 5 songs
    jsonAns = []
    for i in ans:
        jsonAns.append(dict(Title=i))
    return jsonAns
    # return json.dumps([dict(zip(keys, i)) for i in ans])


@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/albums")
def get_albums():
    return list(album_to_songs_jaccard_truncated.keys())


@app.route("/tags")
def get_tags():
    return sorted(good_tags)


@app.route("/songs")
def songs_search():
    # album = request.args.get("album")
    # tags = set(request.args.getlist("tags"))
    # print(tags)

    # jaccard_songs = album_to_songs_jaccard_truncated[album]

    # # adjust songs by tags
    # for i, value in enumerate(jaccard_songs):
    #     song_index = value[0]
    #     jacc_score = value[1]

    #     song_tags = song_index_to_tags[str(song_index)] if str(
    #         song_index) in song_index_to_tags else []
    #     for s in song_tags:
    #         song_tag = s[0]
    #         weight = s[1]
    #         if song_tag in tags:

    #             jacc_score *= 1 * (weight / 100)

    #             print("INCREASING SCORE OF", song_index,
    #                   "to", jacc_score)

    #     jaccard_songs[i] = [song_index, jacc_score]

    # jaccard_songs = sorted(jaccard_songs, reverse=True, key=lambda x: x[1])

    # # get the song indexes, ignoring the jaccard scores
    # song_indexes = [js[0] for js in jaccard_songs]

    # # get song and artist from the indexes
    # songs = [song_index_to_song_title_and_artist[str(
    #     song_index)] for song_index in song_indexes]

    # # get spotify data for the songs
    # spotify_data = []

    # for song in songs:
    #     title = song['title']
    #     artist = song['artist']
    #     data = retrieve_spotify_data_for_frontend(title, artist)
    #     if (data):
    #         spotify_data.append(
    #             retrieve_spotify_data_for_frontend(title, artist))

    #     if (len(spotify_data) >= 10):
    #         break

    # # return spotify data for up to 10 songs that had successful spotify queries
    # return list(spotify_data[:10])
    df = pd.read_csv('p04jaccard.csv')
    df1 = pd.read_csv('p04emotionsocial.csv')
    # query = episode.lower()
    # album = request.args.get("album")
    query = request.args.get("album").lower()
    print(query)
    rows_jac = df.loc[df['Unnamed: 0'].str.lower() == query]
    rows_tags = df1.loc[df1['Unnamed: 0'].str.lower() == query] #tags for songs in album
    size = len(rows_jac)
    for i in range(0, len(rows_jac)):
        for j in range(1, 601):
            cur_jac = rows_jac.iloc[i, j]
            modifier = 1
            if type(rows_tags.iloc[i, 1]) == float:
                emote1 = []
            else:
                emote1 = eval(rows_tags.iloc[i, 1])
            if type(rows_tags.iloc[i, 2]) == float:
                social1 = []
            else:
                social1 = eval(rows_tags.iloc[i, 2])
            if type(df1.iloc[j - 1, 1]) == float:
                emote2 = []
            else:
                emote2 = eval(df1.iloc[j - 1, 1])
            if type(df1.iloc[j - 1, 2]) == float:
                social2 = []
            else:
                social2 = eval(df1.iloc[j - 1, 2])
            emote1 = dict(emote1)
            emote2 = dict(emote2)
            social1 = dict(social1)
            social2 = dict(social2)
            for val in emote2:
                if val in emote1:
                    modifier += .1
                    dif = abs(emote1[val] - emote2[val])
                    modifier += .1 * (1 - .01 * dif)
            for val in social2:
                if val in social1:
                    modifier += .1
                    dif = abs(social1[val] - social2[val])
                    modifier += .1 * (1 - .01 * dif)
            rows_jac.iloc[i, j] = cur_jac * modifier
    tmpSum = rows_jac.sum(numeric_only=True, axis=0)
    tmpAvg = tmpSum.divide(size)
    tmpAns = tmpAvg.to_numpy()
    songs = df.columns.tolist()[1::]
    tples = zip(tmpAns, songs)
    tples = sorted(tples, reverse=True)
    ans = [song for (_, song) in tples[0:15]]
    spotify_data = []
    for song in ans:
        tmp = song.split('-')
        title = tmp[0]
        artist = tmp[1]
        data = retrieve_spotify_data_for_frontend(title, artist)
        if (data):
            spotify_data.append(retrieve_spotify_data_for_frontend(title, artist))
        if (len(spotify_data) >= 10):
            break
    return list(spotify_data[:10])
    # return ans
    # print(ans)
    # jsonAns = []
    # for i in ans:
    #     jsonAns.append(dict(Title = i))
    # return jsonAns

    # # get the top 10 song indexes, ignoring the jaccard scores
    # top_10_song_indexes = [js[0] for js in jaccard_songs[: 10]]

    # # get song and artist for the 10 songs
    # top_10_songs = [song_index_to_song_title_and_artist[str(
    #     song_index)] for song_index in top_10_song_indexes]

    # # get spotify data for top 10 songs
    # spotify_data = []

    # for song in top_10_songs:
    #     title = song['title']
    #     artist = song['artist']
    #     data = retrieve_spotify_data_for_frontend(title, artist)
    #     if (data):
    #         spotify_data.append(
    #             retrieve_spotify_data_for_frontend(title, artist))

    # print(top_10)
    # return list(top_10_songs)


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)


app.run(debug=True)
