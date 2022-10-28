from setting import bot, sp, user_language
# import bot_en
# import bot_it

# Set the language for the bot
global start_txt
start_txt = ''
global top_track_txt
top_track_txt = ''

def check_and_set_language():
    global start_txt
    global top_track_txt

    if(user_language == "it"):
        lan = "txt_it"

        f = open(f"{lan}/welcome.txt", "r")

        start_txt = str(f.read())
        f.close()

        f = open(f"{lan}/top_track.txt", "r")
        top_track_txt = str(f.read())
        f.close()

    elif((user_language == "en") or (user_language.lower() == "none")):
        lan = "txt_en"

        f = open(f"{lan}/welcome.txt", "r")
        start_txt = str(f.read())
        f.close()

        f = open(f"{lan}/top_track.txt", "r")
        top_track_txt = str(f.read())
        f.close()


@bot.message_handler(commands=['start'])
def send_start(message):
    check_and_set_language()
    chat_id = message.chat.id
    
    bot.send_message(chat_id, start_txt)

@bot.message_handler(commands=['top'])
def top_tracks(message):
    bot_lang = check_and_set_language()
    chat_id = message.chat.id
    bot.send_message(chat_id, top_track_txt)
    bot.register_next_step_handler(message, top_track)

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


#Return the URI (a sort of ID) of the artist
def search_artist_id(artist_name) -> str:
    results = sp.search(artist_name, limit= 1, type="artist")
    items = results['artists']['items']
    artist_item = items[0]
    return(str(artist_item['uri']))
# ======================================================


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