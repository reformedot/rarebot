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
from requests import get
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

############################### Bot ############################################

translator = Translator() # Create object of Translator.
base='https://www.orpha.net/consor/cgi-bin/'
url = 'https://www.orpha.net/consor/cgi-bin/Clinics_ERN.php?lng=EN'
response = get(url)    
html_soup = BeautifulSoup(response.text, 'html.parser')
geolocator = Nominatim(user_agent="share4bot")

mapa = StaticMap(500, 500)


center_containers = html_soup.find_all('div', class_ = 'ERN')
first=center_containers[0]

tipus=[]
mal=[]
i=0
for tag in first.ul.find_all("li", recursive=True):     
    if tag.a.has_attr('href'):
        tipus.append(tag.a.text.lower())
        ini=tag.a.text.find('-')
        nom=tag.a.text[ini+2:]
        mal.append('mal%s'%i)
        exec('mal%s={}'%i)
        eval('mal%s'%i)['link']=tag.a.attrs['href']
        i+=1

nums=[]
ciutats=[]
linkk=[]
def check(inf):
    global linkk
    global mapa
    global ciutats
    nums=[]
    for i in tipus:
        if inf in i:
            nums.append(tipus.index(i))
    i='mal'+str(nums[0])
    url = base+eval(i)['link']
    response1 = get(url)
    html_soup1= BeautifulSoup(response1.text, 'html.parser')
    centers = html_soup1.find_all('div', class_ = 'activityLoc')
    first1=centers[0]
    for tag in first1.find_all("div", recursive=True):
        if tag.strong!=None:
             if tag.strong.text not in eval(i):
                 eval(i)[tag.strong.text]=[]
                 pais=tag.strong.text
        if tag.p!=None:
            city=tag.p.text
        if tag.a!=None:
            #if [tag.a.attrs['href'],city] not in eval(i)[pais]:
            if city[:-1] not in eval(i)[pais]:
                eval(i)[pais].append(city[:-1])
                if pais=='ESPAGNE':
                    linkk.append(base+tag.a.attrs['href'])
    ciutats=[]
    for z in eval(i)['ESPAGNE']:
        ciutats.append(z)


         




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
  elif language =='EUS':
    translated = translator.translate(text, dest='eu')
    return translated
  elif language =='GAL':
    translated = translator.translate(text, dest='gl')
    return translated  





def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=translate("Hi! Choose your language typing /idioma + (CAT, ES, FR, EN, EUS, GAL)").text)    

 


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
  bot.sendMessage(chat_id=update.message.chat_id, text=translate("Gracias! El idioma ha sido configurado correctamente").text)    
  #bot.send_contact(chat_id=update.message.chat_id, phone_number= "112", first_name="Teléfono de emergencias")
  


############################ Keyboards #########################################
def main_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton(translate("Informació").text + "🔍", callback_data='info_keyboard_cat')],
              [InlineKeyboardButton(translate("Recursos").text + "♿", callback_data='link_menu_keyboard_cat')],
              [InlineKeyboardButton(translate("Links d\'interès").text + "🌐", callback_data='link_menu_keyboard_cat')],
              [InlineKeyboardButton(translate("Test de concienciación").text+'📚', url='https://forms.gle/tDh1fiKBdpNjG2S67')],
              [InlineKeyboardButton(translate("Donatius").text+'🎉', url='https://www.ccma.cat/tv3/marato/es/2019/230/')]]
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
    global ciutats
    global linkk
    try:
        fitxer = "%d.png" % random.randint(1000000, 9999999)
        lat, lon = update.message.location.latitude, update.message.location.longitude
        mapa.add_marker(CircleMarker((lon, lat), 'blue', 10))
        for k in ciutats:
            location = geolocator.geocode(k)
            mapa.add_marker(CircleMarker((location.longitude,location.latitude), 'red', 10))
        
        imatge = mapa.render()
        imatge.save(fitxer)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
        for p in linkk:
            bot.sendMessage(chat_id=update.message.chat_id, text=p)  
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
  check(malaltia)


def idioma(bot, update): 
    global language
    language=""
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
    else:
      bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I don't speak your language!")
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
updater.dispatcher.add_handler(CallbackQueryHandler(sos_menu_cat))
#updater.dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler('info', info))
#updater.dispatcher.add_handler(CommandHandler('language', language))
updater.dispatcher.add_handler(CommandHandler('idioma', idioma))
updater.dispatcher.add_handler(MessageHandler(Filters.location, where, pass_user_data=True))  

updater.start_polling()
################################################################################
updater.idle()



