import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import numpy as np

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "hc659"
MYSQL_PORT = 3306
MYSQL_DATABASE = "songsdb"

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
    # query_sql = f"""SELECT {episode} FROM jac WHERE LOWER({episode}) LIKE '%%{episode.lower()}%%' limit 10"""
    # query_sql=f"""SELECT * FROM jac WHERE LOWER(FIELD1) LIKE '%%{episode.lower()}%%' limit 10"""
    query_sql=f""" SELECT * FROM jac WHERE LOWER(FIELD1) LIKE '%%{episode.lower()}%%' limit 10"""
    # keys = ["Artist", "Title", "Album", "Year", "Date", "Lyric", "Genre"]
    keys=['FIELD1', 'Dua_Lipa', 'Future_Nostalgia', 'FIELD4', 'Unreleased_Songs', 'a', 'Unreleased_Songss', 'aa', 'aaa', 'Unreleased_Songsss', 'Unreleased_Songssss', 'Unreleased_Songsssss', 'aaaa', 'New_Love_Remixes', 'Sweetener', 'Dangerous_Woman', 'Sweetenerr', 'My_Everything', 'aaaaa', 'Christmas_Kisses_EP', '\u200bk_bye_for_now_swt_live', 'aaaaaa', 'Unreleased_Songssssss', '\u200bk_bye_for_now_swt_livee', 'The_Remix', 'The_Remixx', 'The_Remixxx', 'aaaaaaa', 'aaaaaaaa', 'Voicenotes', 'Ego', 'CP3', 'CP33', 'NBA_2K16_Soundtrack', 'Take_Care', 'aaaaaaaaa', 'The_Best_in_the_World_Pack', 'Take_Caree', 'More_Life', 'Dark_Lane_Demo_Tapes', 'Thank_Me_Later', 'aaaaaaaaaa', 'Dark_Lane_Demo_Tapess', 'Young_Sweet_Jones_2', 'Comeback_Season', 'FIELD46', 'b', 'bb', 'Room_for_Improvement', 'Unreleased_Songsssssss', 'bbb', 'bbbb', 'bbbbb', 'Heartbreak_Drake', 'Unreleased_Songssssssss', 'bbbbbb', 'You_Never_Walk_Alone', 'LOVE_YOURSELF_轉_‘Tear’', 'MAP_OF_THE_SOUL_7', 'MAP_OF_THE_SOUL_7_The_Journey_', 'You_Never_Walk_Alonee', 'MAP_OF_THE_SOUL_77', 'DarkWild', 'YOUTH', 'Young_Forever', 'WAKE_UP', 'Danger_MoBlueMix_feat_THANH_Single', 'bbbbbbb', 'Dynamite_DayTime_Version', 'bbbbbbbb', 'WHEN_WE_ALL_FALL_ASLEEP_WHERE_DO_WE_GO_Japanese_Import', 'dont_smile_at_me', 'bbbbbbbbb', '92nd_Academy_Awards_Performances', 'bbbbbbbbbb', 'FIELD76', 'c', 'Invasion_of_Privacy', 'Gangsta_Bitch_Music_Vol_1_Promo_CD', 'cc', 'Gangsta_Bitch_Music_Vol_1_Promo_CDD', 'Kamikaze', 'Relapse', 'SHADYXV', 'The_Marshall_Mathers_LP2_Deluxe', 'Revival', 'The_Marshall_Mathers_LP', 'Encore', 'The_Slim_Shady_LP', 'Recovery', 'Devil’s_Night', 'Unreleased_Songsssssssss', 'Music_to_Be_Murdered_By_Side_B', 'Music_to_Be_Murdered_By', 'Straight_from_the_Lab_Part_2', 'ccc', 'Invasion_Shady_Times', 'cccc', 'The_Marshall_Mathers_LP_Snippet_Tape', 'The_Marshall_Mathers_LP_Snippet_Tapee', 'ccccc', 'The_Marshall_Mathers_LP_Snippet_Tapeee', 'cccccc', 'ccccccc', 'cccccccc', 'ccccccccc', 'cccccccccc', 'The_Fame', 'The_Famee', 'ARTPOP', 'Born_This_Way', 'Artpop_Act_II_Scrapped', 'FIELD113', 'd', 'Unreleased_Songssssssssss', 'Artpop_Act_II_Scrappedd', 'Unreleased_Songsssssssssss', 'dd', 'Unreleased_Songst', 'ddd', 'Unreleased_Songstt', 'Unreleased_Songsttt', 'Bad_Romance_The_Remixes_Pt_1_2', 'The_Remixxxx', 'dddd', 'ddddd', 'dddddd', 'The_Pinkprint', 'The_Pinkprinttt', 'Pink_Friday_Roman_Reloaded', 'Pink_Friday_Roman_Reloaded_The_ReUp', 'Beam_Me_Up_Scotty', 'Pink_Friday_Roman_Reloadedd', 'Sucka_Free', 'ddddddd', 'Unreleased_Songstttt', 'Unreleased_Songsttttt', 'Playtime_is_Over', 'Unreleased_Songstttttt', 'Unreleased_Songsttttttt', 'dddddddd', 'ddddddddd', 'dddddddddd', 'BEYONCÉ', 'B’Day', 'Four', 'I_Am_Sasha_Fierce', 'Unreleased_Songsa', 'Dangerously_In_Love', 'FIELD150', 'HOMECOMING_THE_LIVE_ALBUM', 'Dangerously_In_Lovee', 'e', 'ee', 'HOMECOMING_THE_LIVE_ALBUMM', 'B’Dayy', '4_The_Remix_EP', 'The_Fighting_Temptations_Music_from_the_Motion_Picture', 'eee', 'The_Beyoncé_Experience_Live', 'eeee', 'I_Am_World_Tour', 'eeeee', 'Swaggot_Trilltape', 'Songs_About_Jane', 'Overexposed', 'It_Won’t_Be_Soon_Before_Long', 'Songs_About_Janee', 'Hands_All_Over', 'eeeeee', 'Call_and_Response_The_Remix_Album', 'Songs_About_Jane_10th_Anniversary_Edition', 'Call_and_Response_The_Remix_Albumm', 'eeeeeee', '÷_Divide', '×_Multiply', '_Plus', '_Pluss', 'eeeeeeee', 'eeeeeeeee', 'Loose_Change_EP', 'eeeeeeeeee', 'FIELD183', 'f', 'Want_Some_EP', 'Bridget_Jones’s_Baby_Original_Motion_Picture_Soundtrack', 'ff', 'fff', 'Purpose_Deluxe', 'My_Worlds_The_Collection', 'Purpose_Deluxee', 'ffff', 'My_World_20', 'Believe', 'Under_the_Mistletoe', 'fffff', 'Unreleased_Songstttttttt', 'Unreleased_Songsttttttttt', 'ffffff', 'fffffff', 'Unreleased_Songstttttttttt', 'Boyfriend_Remixes', 'JB6', 'JB66', 'ffffffff', 'fffffffff', 'evermore', 'reputation', 'Lover', 'Fearless', 'Red_Deluxe_Edition', 'ffffffffff', 'Red_Deluxe_Editionn', 'Taylor_Swift', 'The_Hunger_Games_Songs_from_District_12_and_Beyond', 'Unreleased_Songsu', 'FIELD217', 'Unreleased_Songsuu', 'Unreleased_Songsuuu', '2004_Demo_CD_Three_Songs', 'Unreleased_Songsuuuu', 'Speak_Now_World_Tour_Live_Brazilian_Edition', 'g', 'gg', 'ggg', 'folklore_the_long_pond_studio', 'folklore_the_long_pond_studioo', 'folklore_the_long_pond_studioooo', 'Speak_Now_World', 'Live_From_Clear', 'Revivall', 'Revivalll', 'Stars_Dance', 'gggg', 'Wizards_of_Waverly_Place', 'Chill_Mood', 'ggggg', 'Same_Old_Love_Remixes', 'Hands_to_Myself_Remixes', 'Kaleidoscope_EP', 'XY', 'Viva_La_Vida_or_Death_and_All_His_Friends', 'XYY', 'Game_of_Thrones_The_Musical', 'gggggg', 'Mylo_Xyloto', 'Super_Bowl_Halftime_Shows', 'Talk', 'Live_in_Madrid', 'Live_In_Buenos_Aires', 'Mince_Spies_EP', 'Unreleased_Songsuuuuu', 'Unreleased_Songsuuuuuu', 'ggggggg', 'Rhythms_del_Mundo_Revival', 'Trouble_‒_Norwegian_Live_EP', 'ANTI', 'Unapologetic', 'Unapologeticc', 'Talk_That_Talk', 'Love_on_the_Brain_Dance_Remixes', 'Good_Girl_Gone_Bad', 'Music_of_the_Sun_UK_Edition', 'Music_of_the_Sun_UK_Editionn', 'What_Now_Remixes_Part_2', 'Desperado_Dance_Remixes', 'This_Is_Rihanna_The_Mixtape', 'Rated_R_Remixed', 'Needed_Me_Dance_Remix', 'Needed_Me_Dance_Remixx', 'You_da_One_Remixes', 'Unreleased_Songsuuuuuuu', 'You_da_One_Remixess', 'SM_Remixes', 'ROCKSTAR_101_The_Remixes', 'You_da_One_Remixesss', 'One_of_the_Boys', 'Witness', 'Witnesss', 'Teenage_Dream', 'Smile_Deluxe_Edition', 'gggggggg', 'ggggggggg', 'gggggggggg', 'Ur_So_Gay_EP', 'The_One_That_Got_Away_The_Remixes_EP', 'The_Hello_Katy_Australian_Tour_EP', 'ET_The_Remixes_EP', 'A_Katy_Perry_Shelved', 'Fingerprints_Shelved', 'Unreleased_Songsuuuuuuuu', 'Waking_Up_in_Vegas_The_Remixes_EP', 'Hollywood’s_Bleeding', 'beerbongs_bentleys', 'Hollywood’s_Bleedingg', 'FIELD296', 'Unreleased_Songsuuuuuuuuu', 'Unreleased_Songsuuuuuuuuuu', 'Unreleased_Songsv', 'h', 'Free_Spirit']
    data = mysql_engine.query_selector(query_sql)
    # print(data)
    # print("====================================")
    # print(data)
    # print("=======================================")
    # print([dict(zip(keys,i))] for i in data)
    return json.dumps([dict(zip(keys, i)) for i in data],default=str)


@app.route("/")
def home():
    return render_template('base.html', title="sample html")


@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)


app.run(debug=True)
