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
from googletrans import Translator

############################### Bot ############################################

translator = Translator() # Create object of Translator.


language="EN"

def translate(text):
  if language == "ES":
    translated = translator.translate(text, dest='es')
    return translated
  elif language == "EN":
    translated = translator.translate(text, dest='en')
    return translated
  elif language =="CAT":
    translated = translator.translate(text, dest='ca')
    return translated
  elif language =='FR':
    translated = translator.translate(text, dest='fr')
    return translated




def start(bot, update):
  update.message.reply_text(translate(main_menu_message_cat()).text, #1r param: missatge 
                            reply_markup=main_menu_keyboard_cat())#2n param: botons 
 


def main_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id, #1r param: missatge 
                        text=translate(main_menu_message_cat()).text,
                        reply_markup=main_menu_keyboard_cat()) #1r param: menú keyboard al que anem al pulsar 

def link_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=translate(link_menu_message_cat()).text,
                        reply_markup=link_menu_keyboard_cat())

def rrss_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=translate(rrss_menu_message()).text,
                        reply_markup=rrss_menu_keyboard_cat()) 



def sos_menu_cat(bot, update):
  query = update.callback_query
  bot.send_contact(chat_id=query.message.chat_id, phone_number= "112", first_name="Teléfono de emergencias")
  


############################ Keyboards #########################################
def main_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton(translate("Informació").text + "🔍", callback_data='info_keyboard_cat')],
              [InlineKeyboardButton(translate("Recursos").text + "♿", callback_data='link_menu_keyboard_cat')],
              [InlineKeyboardButton(translate("Links d\'interès").text + "🌐", callback_data='link_menu_keyboard_cat')],
              [InlineKeyboardButton(translate("SOS").text+'📞', callback_data='sos_menu_cat')],
              [InlineKeyboardButton(translate("Test de concienciación").text+'📚', url='https://forms.gle/tDh1fiKBdpNjG2S67')],
              [InlineKeyboardButton(translate("Donatius").text+'🎉', url='https://www.ccma.cat/tv3/marato/es/2019/230/')]]
              #[InlineKeyboardButton('BACK', callback_data='BACK_Keyboard_cat')]
  return InlineKeyboardMarkup(keyboard)


def link_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton(translate('Xarxes Socials').text + "📱", callback_data='rrss_menu_keyboard_cat')],
              [InlineKeyboardButton(translate('Associacions').text + "🚻", callback_data='main_menu_cat')],
              [InlineKeyboardButton(translate('Links d\'interès').text + "🌐", url = "https://www.share4rare.org/")],
              [InlineKeyboardButton(translate('Libro de la cigüeña añil').text+'📖', url="https://weeblebooks.com/es/educacion-emocional/la-ciguena-anil/")],
              [InlineKeyboardButton(translate('BACK').text + " 🔙", callback_data='main_menu_cat')]]
  return InlineKeyboardMarkup(keyboard)

def rrss_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton('Instagram', url="https://www.instagram.com/share4rare/")],
              [InlineKeyboardButton('Twitter', url="https://twitter.com/share4rare")],
              [InlineKeyboardButton('Facebook', url = "https://bit.ly/2PHPZr6")],
              [InlineKeyboardButton('LinkedIn', url="https://www.linkedin.com/company/share4rare")],
              [InlineKeyboardButton('WhatsApp', url="https://bit.ly/36ArtyU")],
              [InlineKeyboardButton('BACK🔙', callback_data='link_menu_keyboard_cat')]]
  return InlineKeyboardMarkup(keyboard)  

 
"""
def language(bot, update):
    languageentrada = update.message.text[6:]
    if languageentrada == "ES":
      language = "ES"
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "CAT":
      language = "CAT"
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "FR":
      language = "FR"
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "EUS":
      language = "EUS"
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "EN":
      language = "EN"
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
    else :
      bot.sendMessage(chat_id=update.message.chat_id, text=Translate("Gracias! El idioma ha sido configurado correctamente").text)
"""


#########################EXTRA#############################

def echo(bot, update):
  print(update.message.text)
  bot.send_message(chat_id=update.message.chat_id, text=translator.translate(update.message.text))



def where(bot, update, user_data):
    try:
        fitxer = "%d.png" % random.randint(1000000, 9999999)
        lat, lon = update.message.location.latitude, update.message.location.longitude
        mapa = StaticMap(500, 500)
        mapa.add_marker(CircleMarker((lon, lat), 'blue', 10))
        mapa.add_marker(CircleMarker((-3.7025600, 40.4165000), 'red', 10))
        mapa.add_marker(CircleMarker((9.0000000, 51.0000000), 'red', 10))
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
"""
# and so on for every callback_data option

malaltia=""
def info(bot, update):
  malaltia = update.message.text[6:]
  print(malaltia)

def idioma(bot, update): 
    global language
    languageentrada = update.message.text[8:]
    if languageentrada == "ES":
      language = "ES"
      print("123")
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)    
    elif languageentrada == "CAT":
      language = "CAT"
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "FR":
      language = "FR"
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "EUS":
      language = "EUS"
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)
    elif languageentrada == "EN":
      language = "EN"
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)
    else :
      bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)
    update.message.reply_text(translate(main_menu_message_cat()).text, #1r param: missatge 
                            reply_markup=main_menu_keyboard_cat())()


""" 
def info2(bot, update):
  print("aquest si")
"""

############################# Messages #########################################
def main_menu_message_cat():
  return "Hola! Benvingut a RareBot!\n Pots buscar Informació d\'enfermetats minoritàries, buscar Material, veure els Links d\'interès, fer  un Test de concienciació o fer Donatius!"

def link_menu_message_cat():
  return "Escull què vols!"

def link_menu_message():
  return 'Aquí pots trobar diferents links d \'interès'


def rrss_menu_message():
  return 'Xarxes socials... aquí en tens unes quantes!'

############################# Handlers #########################################

TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu_cat, pattern='main_menu_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(link_menu_cat, pattern='link_menu_keyboard_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(rrss_menu_cat, pattern='rrss_menu_keyboard_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(sos_menu_cat, pattern = 'sos_menu_cat'))
updater.dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler('info', info))
#updater.dispatcher.add_handler(CommandHandler('language', language))
updater.dispatcher.add_handler(CommandHandler('idioma', idioma))
  

updater.start_polling()
################################################################################
updater.idle()



