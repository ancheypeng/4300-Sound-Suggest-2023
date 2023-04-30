import pylast
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = "a07dd83a31cdd7e40f4620c5bf852459"  
SHARED_SECRET = "f0f192c5139289e6b2ce1159e00a7563"

username = "Sound-Suggest"
password_hashed = pylast.md5("8#45jVk!5Se8B&Rw")

last_fm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=SHARED_SECRET,
    username=username,
    password_hash=password_hashed
)
def get_lastfm_tags(song_artist, song_name):
    tag_weights = []
    song = last_fm_network.get_track("Iron Maiden", "The Nomad")
    for entry in song.get_top_tags():
        tag_name = entry[0].get_name()
        weight = entry[1]
        tup = (tag_name, weight)
        tag_weights.append(tup)

    return tag_weights




