from setting import bot, sp, user_language
import bot_en
import bot_it

# Set the language for the bot
def check_and_set_language():
    if(user_language == "it"):
        return bot_it
    elif((user_language == "en") or (user_language.lower() == "none")):
        return bot_en

bot_lang = check_and_set_language()

@bot.message_handler(commands=['start'])
def send_start(message):
    bot_lang = check_and_set_language()
    chat_id_tmp = message.chat.id
    bot_en.init(chat_id_tmp)
    bot_it.init(chat_id_tmp)
    
    bot_lang.send_start()

@bot.message_handler(commands=['top'])
def top_tracks(message):
    bot_lang = check_and_set_language()
    chat_id_tmp = message.chat.id
    bot_en.init(chat_id_tmp)
    bot_it.init(chat_id_tmp)

    bot_lang.send_top_tracks()
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
        buffer += str(idx + 1)+ " " + track['name'] + "\n"

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
    bot_lang = bot_it
    global user_language
    user_language = 'it'

# Change the language to english
@bot.message_handler(commands=['eng'])
def set_language(message):
    #print("Set to english")
    bot.send_message(message.chat.id, "Set english as language")
    bot_lang = bot_en
    global user_language
    user_language = 'en'
    
bot.polling()