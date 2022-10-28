import telebot
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Insert your CID and SECRET CID from Spotify For Developers
cid = "Insert your CID"
cid_secret = "Insert your SECRET CID"

# Insert your Bot Token taken from BotFather
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
