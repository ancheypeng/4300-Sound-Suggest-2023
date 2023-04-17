import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import pandas as pd
import numpy as np

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

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this

with open('../dataset/jsons/album_to_songs_jaccard_truncated.json', 'r') as fp:
    album_to_songs_jaccard_truncated = json.load(fp)

with open('../dataset/jsons/song_index_to_song_title_and_artist.json', 'r') as fp:
    song_index_to_song_title_and_artist = json.load(fp)

with open('../dataset/jsons/song_index_to_tags.json', 'r') as fp:
    song_index_to_tags = json.load(fp)


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


@app.route("/songs")
def songs_search():
    album = request.args.get("album")
    tags = set(request.args.getlist("tags"))
    print(tags)

    jaccard_songs = album_to_songs_jaccard_truncated[album]

    # adjust songs by tags
    for i, value in enumerate(jaccard_songs):
        song_index = value[0]
        jacc_score = value[1]

        song_tags = song_index_to_tags[str(song_index)] if str(
            song_index) in song_index_to_tags else []
        for s in song_tags:
            song_tag = s[0]
            weight = s[1]
            if song_tag in tags:
                print("INCREASING SCORE OF", song_index,
                      "to", jacc_score * 2 * (weight / 100))
                jacc_score *= 2 * (weight / 100)

        jaccard_songs[i] = [song_index, jacc_score]

    jaccard_songs = sorted(jaccard_songs, reverse=True, key=lambda x: x[1])

    top_10 = jaccard_songs[: 10]
    # print(top_10)
    return list(top_10)


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)


# app.run(debug=True)
