import datetime

import telegram
import time
import webbrowser
import random
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler,  MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from staticmap import StaticMap, CircleMarker

############################### Bot ############################################



def start(bot, update):
  webbrowser.open('http://inventwithpython.com/')
  update.message.reply_text(main_menu_message_cat(), #1r param: missatge 
                            reply_markup=main_menu_keyboard_cat())#2n param: botons 

  #time.sleep(1.2)
 


def main_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id, #1r param: missatge 
                        text=main_menu_message_cat(),
                        reply_markup=main_menu_keyboard_cat()) #1r param: menú keyboard al que anem al pulsar 

def link_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=link_menu_message_cat(),
                        reply_markup=link_menu_keyboard_cat())

def rrss_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=rrss_menu_message(),
                        reply_markup=rrss_menu_keyboard_cat()) 

 

############################ Keyboards #########################################
def main_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton('Informació🔍', callback_data='info_keyboard_cat')],
              [InlineKeyboardButton('Recursos♿', callback_data='recursos_keyboard_cat')],
              [InlineKeyboardButton('Links d\'interès🌐', callback_data='link_menu_keyboard_cat')],
              [InlineKeyboardButton('SOS📞', callback_data='sos_keyboard_cat')],
              [InlineKeyboardButton('Test de concienciació📚', callback_data='test_keyboard_cat')],
              [InlineKeyboardButton('Donatius🎉', callback_data='donatiu_keyboard_cat')]]
              #[InlineKeyboardButton('BACK', callback_data='BACK_Keyboard_cat')]
  return InlineKeyboardMarkup(keyboard)


def link_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton('Xarxes Socials📱', callback_data='rrss_menu_keyboard_cat')],
              [InlineKeyboardButton('Associacions🚻', callback_data='main_menu_cat')],
              [InlineKeyboardButton('Links d\'interès🌐', url = "https://www.share4rare.org/")],
              [InlineKeyboardButton('Llibre la cigüeña añil📖', url="https://weeblebooks.com/es/educacion-emocional/la-ciguena-anil/")],
              [InlineKeyboardButton('BACK🔙', callback_data='m1')]]
  return InlineKeyboardMarkup(keyboard)

def rrss_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton('Instagram', url="https://www.instagram.com/share4rare/")],
              [InlineKeyboardButton('Twitter', url="https://twitter.com/share4rare")],
              [InlineKeyboardButton('Facebook', url = "https://bit.ly/2PHPZr6")],
              [InlineKeyboardButton('LinkedIn', url="https://www.linkedin.com/company/share4rare")],
              [InlineKeyboardButton('WhatsApp', url="https://bit.ly/36ArtyU")],
              [InlineKeyboardButton('BACK🔙', callback_data='rrss_menu_keyboard_cat')]]
  return InlineKeyboardMarkup(keyboard)  



def link_link_rrss():
  bot.send_message(chat_id=chat_id, 
                 text="*bold* _italic_ `fixed width font` [link](http://google.com).", 
                 parse_mode=telegram.ParseMode.MARKDOWN)  


"""

def where(bot, update, user_data):
    try:
        fitxer = "%d.png" % random.randint(1000000, 9999999)
        lat, lon = update.message.location.latitude, update.message.location.longitude
        mapa = StaticMap(500, 500)
        mapa.add_marker(CircleMarker((lon, lat), 'blue', 10))
        imatge = mapa.render()
        imatge.save(fitxer)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
        os.remove(fitxer)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣') 
"""

def where(bot, update, user_data):
    lat, lon = update.message.location.latitude, update.message.location.longitude
    print(lat, lon)
    bot.send_message(chat_id=update.message.chat_id, text='Ets a les coordenades %f %f' % (lat, lon))   

# and so on for every callback_data option

############################# Messages #########################################
def main_menu_message_cat():
  return 'Hola! Benvingut a RareBot!\n Pots buscar Informació🔍 d\'enfermetats minoritàries, buscar Material♿, veure els Links d\'interès🌐, fer  un Test de concienciació📚 o fer Donatius🎉! ")'

def link_menu_message_cat():
  return 'Escull què vols!'

def second_menu_message():
  return 'Choose the submenu in second menu:'

def link_menu_message():
  return 'Aquí pots trobar diferents links d \'interès🌐'


def rrss_menu_message():
  return 'Choose the submenu in second menu:'

############################# Handlers #########################################

TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu_cat, pattern='main_menu_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(link_menu_cat, pattern='link_menu_keyboard_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(link_link_rrss, pattern='m4'))
updater.dispatcher.add_handler(CallbackQueryHandler(rrss_menu_cat, pattern='rrss_menu_keyboard_cat'))
updater.dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))

updater.start_polling()
################################################################################




