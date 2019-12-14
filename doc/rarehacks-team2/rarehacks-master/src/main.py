import telegram
import pandas as pd
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters, ConversationHandler
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.response_selection import get_most_frequent_response
from fuzzywuzzy.process import extractOne
from haversine import haversine

import os

if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')



chatbot = ChatBot("RareHacks", response_selection_method = get_most_frequent_response)
db = pd.read_csv("data/keywords.csv")
db.columns = ['keyword','general answer','diffuse leptomeningeal melanocytosis',
    'familial melanoma','uveal melanoma']
places = pd.read_csv('data/places.csv')
places.columns = ['keyword','diffuse leptomeningeal melanocytosis',
    'familial melanoma','uveal melanoma']

locations = {"GERMANY":         (50, 10),
             "BELGIUM":         (50, 4),
             "AUSTRIA":         (47, 14),
             "SPAIN":           (41.5, 2),
             "CANADA":          (58, -106),
             "ESTONIA":         (58, 26),
             "FRANCE":          (46, 3),
             "ITALY":           (41, 13),
             "HUNGARY":         (47, 19),
             "ISRAEL":          (31, 34),
             "JAPAN":           (36, 138),
             "THE NETHERLANDS": (52, 6),
             "POLAND":          (52, 19),
             "PORTUGAL":        (39, -8),
             "UNITED KINGDOM":  (53, -1),
             "SWITZERLAND":     (62, 15),
             "TURKEY":          (39, 35),
             "LETONIA":         (56, 25)}




trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")
trainer.train("data/preguntasrespuestas.yml")
trainer.train("data/preguntasrespuestas.yml")

NAME, MELANOMA, STAGE, LOCATION = range(4)

def log_in_out(f):
    def g(*args, **kwargs):
        print(f.__name__)
        ret = f(*args,**kwargs)
        print(ret)
        return ret
    return g


def name(bot, update, user_data):
    try:
        name = update.message.text
        user_data["name"] = name
        bot.send_message(chat_id=update.message.chat_id, text="Which kind of melanoma do you want to know about?")
        return MELANOMA
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))
@log_in_out
def start(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id, text="Hi, I'm melabot 😊, I'm here to help you with your melanoma doubts")
        bot.send_message(chat_id=update.message.chat_id, text="What's your name?")
        return NAME
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

@log_in_out
def melanoma(bot, update, user_data):
    try:
        mel = update.message.text
        mel, prob = extractOne(mel,['diffuse leptomeningeal melanocytosis',
                            'familial melanoma',
                            'uveal melanoma'])
        user_data['melanoma'] = 'general answer' if prob < 50 else mel
            
        bot.send_message(chat_id=update.message.chat_id, text="Please, send me your location")
        return LOCATION
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

import traceback

@log_in_out
def location(bot, update, user_data):
    def apply_replace(string, pair):
            token, f = pair
            return string.replace(token, f(user_data))
    try:
        lat, lon = update.message.location.latitude, update.message.location.longitude
        user_data['location'] = (lat, lon)
        message = db[db['keyword'] == 'Hello'][user_data["melanoma"]].values[0]
        message = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], message)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        bot.send_message(chat_id=update.message.chat_id, text="Otherwise, tell me how can I help you")

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))

    return ConversationHandler.END


@log_in_out
def cancel(bot, update):

    bot.send_message(chat_id=update.message.chat_id, 
                     text="I hope you know what you're doing")

    return ConversationHandler.END

from functools import reduce

@log_in_out
def answers(bot, update, user_data, _early_response=[None]):
    try:
        print(update.message.text)
        response = chatbot.get_response(update.message.text)

        if response.confidence < 0.1:
            bot.send_message(chat_id=update.message.chat_id, text="Sorry 🤔, I couldn't understand your question")
            return 

        def apply_replace(string, pair):
            token, f = pair
            return string.replace(token, f(user_data))
    
        keyword = response.text.split("/")[0]

        if keyword == "Centers":
            nearest_location_name = min(locations.keys(), key=lambda x: haversine(locations[x], user_data['location']))
            query = places[places['keyword'] == nearest_location_name]
            info = query[user_data["melanoma"]].values[0]
            info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
            message = "{}:{}.".format(info.split(':')[0], ', '.join(info.split(':')[1].split(', ')[:5]))
            bot.send_message(chat_id=update.message.chat_id, text=message)
        elif keyword == 'more' and 'Centers' in _early_response:
            nearest_location_name = min(locations.keys(), key=lambda x: haversine(locations[x], user_data['location']))
            query = places[places['keyword'] == nearest_location_name]
            info = query[user_data["melanoma"]].values[0]
            info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
            message = "{}:{}.".format(message.split(':')[0], ', '.join(message.split(':')[1].split(', ')[5:]))
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            query = db[db['keyword'] == keyword]
            print(keyword)
            print(query)
            print(user_data["melanoma"])
            if not query.empty:
                info = query[user_data["melanoma"]].values[0]
                info = reduce(apply_replace, [("{NOM}", lambda x: user_data['name']),], info)
                for message in filter(lambda x: len(x.replace(" ","")) > 0 , info.split('. ')):
                    bot.send_message(chat_id=update.message.chat_id, text=message)
            else:
                bot.send_message(chat_id=update.message.chat_id, text=response.text)
        _early_response = [keyword]
    except Exception as e:
        print(e)
        traceback.print_exc()
        bot.send_message(chat_id=update.message.chat_id, text="💣{}".format(str(e)))
def main():
    
    token = open('token.txt').read().strip()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states = {
            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],
            MELANOMA: [MessageHandler(Filters.text, melanoma, pass_user_data=True)],
            LOCATION: [MessageHandler(Filters.location, location, pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, answers, pass_user_data=True))
    
    updater.start_polling()

if __name__ == '__main__':
    main()