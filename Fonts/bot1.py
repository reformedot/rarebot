import datetime

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
############################### Bot ############################################
def start(bot, update):
  update.message.reply_text(main_menu_message_cat(), #1r param: missatge 
                            reply_markup=main_menu_keyboard_cat())#2n param: botons 

  bot.send_message(chat_id=update.message.chat_id, text="Pots escollir Informació🔍, buscar Material♿ o fer Donatius🎉! ")

  
  

def main_menu_cat(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id, #1r param: missatge 
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard_cat()) #1r param: menú keyboard al que anem al pulsar 

def first_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def second_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=second_menu_message(),
                        reply_markup=second_menu_keyboard())

# and so on for every callback_data option
def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass

############################ Keyboards #########################################
def main_menu_keyboard_cat():
  keyboard = [[InlineKeyboardButton('Informació🔍', callback_data='Info_Keyboard_cat')],
              [InlineKeyboardButton('Donatius🎉', callback_data='Donatiu_Keyboard_cat')],
              [InlineKeyboardButton('Recursos♿', callback_data='Recursos_Keyboard_cat')],
              [InlineKeyboardButton('Links d\'interès🌐', callback_data='Link_Keyboard_cat')],
              [InlineKeyboardButton('Test de concienciació📚', callback_data='Test_Keyboard_cat')],
              [InlineKeyboardButton('SOS📞', callback_data='SOS_Keyboard_cat')]]
              #[InlineKeyboardButton('BACK', callback_data='BACK_Keyboard_cat')]
  return ReplyKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message_cat():
  return 'Hola! Benvingut a RareBot!'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'

############################# Handlers #########################################



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu_cat, pattern='main_menu_cat'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))

updater.start_polling()
################################################################################




