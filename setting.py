import telebot
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Token
# Access Token Spotify for developer
cid = "Insert your CID"
cid_secret = "Insert your SECRET CID"

API_TOKEN = "Insert your telegram bot token"

# Spotipy setting
global sp 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= cid, client_secret= cid_secret))

global bot 
bot = telebot.TeleBot(API_TOKEN)

#Get the language of the user
user = bot.get_me()
global user_language
user_language = str(user.language_code)
