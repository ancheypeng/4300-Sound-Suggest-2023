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
MYSQL_USER_PASSWORD = "MayankRao16Cornell.edu"
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this


def sql_search(episode):
    # query_sql = f"""SELECT * FROM mytable WHERE LOWER( Album ) LIKE '%%{episode.lower()}%%' limit 10"""
    # keys = ["Artist", "Title", "Album", "Year", "Date", "Lyric", "Genre"]
    # data = mysql_engine.query_selector(query_sql)
    # return json.dumps([dict(zip(keys, i)) for i in data])
    df = pd.read_csv('jaccard1.csv') 
    query = episode.lower()
    tmp = df.loc[df['Unnamed: 0'].str.lower() == query] #creates new dataframe of only rows of songs inside album specified by query
    size = len(tmp)
    tmpSum = tmp.sum(numeric_only=True, axis=0) #gets sum of all columns 
    tmpAvg = tmpSum.divide(size) #gets avg of all columns
    tmpAns = tmpAvg.to_numpy()
    songs = df.columns.tolist()[1::]
    tples = zip(tmpAns, songs) #tple list (jac val, song name)
    tples = sorted(tples, reverse=True)
    ans = [song for (_, song) in tples[0:10]] #list of only top 5 songs
    jsonAns = []
    for i in ans:
        jsonAns.append(dict(Title = i))
    return jsonAns
    # return json.dumps([dict(zip(keys, i)) for i in ans])



@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)


# app.run(debug=True)
