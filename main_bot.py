from ast import parse
from setting import bot, sp, user_language
# import bot_en
# import bot_it

# Set the language for the bot
global start_txt #For /start
start_txt = ''
global top_track_txt #For /top
top_track_txt = ''
global change_lang_txt #When you use /start send a messager if you want change the language
change_lang_txt = ''
global info_album_txt
info_album_txt = ''

def check_and_set_language():
    global start_txt
    global top_track_txt
    global change_lang_txt
    global info_album_txt

    if(user_language == "it"):
        lan = "txt_it"
    elif((user_language == "en") or (user_language.lower() == "none")):
        lan = "txt_en"

    f = open(f"{lan}/welcome.txt", "r")
    start_txt = str(f.read())
    f.close()

    f = open(f"{lan}/top_track.txt", "r")
    top_track_txt = str(f.read())
    f.close()

    f = open(f"{lan}/change_lang.txt", "r")
    change_lang_txt = str(f.read())
    f.close()

    f = open(f"{lan}/info_album.txt", "r")
    info_album_txt = str(f.read())
    f.close()


@bot.message_handler(commands=['start'])
def bot_send_start(message):
    check_and_set_language()
    chat_id = message.chat.id

    bot.send_message(chat_id, start_txt, parse_mode= "markdown")
    bot.send_message(chat_id, change_lang_txt)

@bot.message_handler(commands=['top'])
def bot_top_tracks(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, top_track_txt)
    bot.register_next_step_handler(message, top_track)

@bot.message_handler(commands=['infoalbum'])
def bot_info_album_txt(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, info_album_txt)
    bot.register_next_step_handler(message, info_album)

# ================== TOP 5 TRACKS ==================
def top_track(message):
    try:
        chat_id_tmp = message.chat.id
        input_text = str(message.text)
        artist_id = search_artist_id(input_text)
        results = sp.artist_top_tracks(artist_id)
    except Exception as e:
        bot.send_message(chat_id_tmp, "There was an error!")
        raise e("Invalid text")

    buffer = '' #Buffer for send the message
    for idx, track in enumerate(results['tracks'][:5]):
        buffer += str(idx + 1) + " - " + track['name'] + "\n"

    bot.send_message(chat_id_tmp, buffer)
# ======================================================

# ================== INFO ALBUM ==================
def info_album(message):
    try:
       chat_id = message.chat.id
       input_text = message.text
       album_id = search_album_id(str(input_text))
       results = sp.album(album_id)
    except Exception as e:
       bot.send_message(chat_id, "There was an error!")
       raise e("Invalid text")

    album_result = results

    #Caption to send the message
    name_album_txt = "Nome dell'album: " + str(album_result['name'])
    total_tracks_txt = "Numero di tracce totali: " + str(album_result['total_tracks'])
    release_data_txt = "Data di rilascio: " + str(album_result['release_date'])
    caption = name_album_txt + "\n" + total_tracks_txt + "\n" + release_data_txt

    image_url = album_result['images'][0]['url']

    bot.send_photo(chat_id, image_url, caption)
# ======================================================

# Return the URI (a sort of ID) of the artist
def search_artist_id(artist_name) -> str:
    results = sp.search(artist_name, limit= 1, type="artist")
    items = results['artists']['items']
    artist_item = items[0]
    return(str(artist_item['uri']))

# Return the URI of the album
def search_album_id(nome_album) -> str:
    results = sp.search(nome_album, limit= 1, type="album")
    items = results['albums']['items']
    album_item = items[0]
    return(str(album_item['uri']))

# Bot commands for change the language

# Change the language to italian
@bot.message_handler(commands=['ita'])
def set_language(message):
    # print("Set to italian")
    bot.send_message(message.chat.id, "Lingua settata in italiano")
    global user_language
    user_language = 'it'
    check_and_set_language()

# Change the language to english
@bot.message_handler(commands=['eng'])
def set_language(message):
    #print("Set to english")
    bot.send_message(message.chat.id, "Set english as language")
    global user_language
    user_language = 'en'
    check_and_set_language()
    
bot.polling()