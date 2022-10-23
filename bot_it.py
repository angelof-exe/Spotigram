from setting import bot,user_language

lan = "txt_it"

f = open(f"{lan}/welcome.txt", "r")
start_txt = str(f.read())
f.close()

f = open(f"{lan}/top_track.txt", "r")
top_track_txt = str(f.read())
f.close()

chat_id = ''

def init(_chat_id):
    global chat_id 
    chat_id = _chat_id

def send_start():
    bot.send_message(chat_id, start_txt)
    bot.send_message(chat_id, "If this isn't your language, use /eng to set the english language!")

def send_top_tracks():
    bot.send_message(chat_id, top_track_txt)



