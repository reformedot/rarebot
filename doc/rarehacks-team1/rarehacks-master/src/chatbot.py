# importing Telegram API
import csv
import numpy as np
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import finder
from bert_serving.client import BertClient

def location(bot, update):
	print(update.message.location)
	bot.send_message(chat_id=update.message.chat_id, text="")
	poi = finder.find(lat=update.message.location.latitude, lng=update.message.location.longitude)


def echo(bot, update):
	print(update.message.text)
	bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

# TELEGRAM STUFF
TOKEN_FILE = 'token.txt'
TOKEN = None
tel_updater = None

# BERT STUFF
bert_client = None
questions = []
answers = []

# DATA FILES
QUESTIONS_FILE = '../data/questions.csv'
ANSWERS_FILE = '../data/answers.csv'

first_message = True
language = 'en'

def com_handler(bot, update):
	text = update.message.text
	print('Original question: {}'.format(text))
	doc_vecs = []
	if first_message:
		global language
		language = update.message.from_user.language_code
		doc_vecs = bert_client.encode([x[0] for x in questions])
		global first_question
		first_question = False
	query_vec = bert_client.encode([text])[0]
    # compute normalized dot product as score
	topk = 5
	score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
	topk_idx = np.argsort(score)[::-1][:topk]
	print(questions[topk_idx[0]][0])
	for idx in topk_idx:
		print('> %s\t%s' % (score[idx], questions[idx]))

	bot.send_message(chat_id=update.message.chat_id, text=questions[topk_idx[0]][0])

	#bot.send_contact(chat_id=update.message.chat_id, phone_number= "112", first_name="Teléfono de emergencias")
	#location_keyboard = telegram.KeyboardButton(text="Share your location", request_location=True)
	#custom_keyboard = [[location_keyboard]]
	#inline_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	#bot.send_message(chat_id=update.message.chat_id, text="Would you be so kind as to share your location?", reply_markup=inline_markup)

def init_chatbot():
	# Read the token file
	with open(TOKEN_FILE) as f_token:
		global TOKEN; TOKEN = f_token.readline().rstrip();
		global tel_updater; tel_updater = Updater(token=TOKEN)
		tel_updater.dispatcher.add_handler(CommandHandler('chatbot', com_handler))
		tel_updater.dispatcher.add_handler(MessageHandler(Filters.location, location))
		tel_updater.dispatcher.add_handler(MessageHandler(Filters.all, com_handler))

def load_questions():
	print('Loading questions...')
	with open(QUESTIONS_FILE) as csv_questions:
		readCSV = csv.reader(csv_questions, delimiter=';')
		next(readCSV)
		for line in readCSV:
			questions.append( (line[1].rstrip(),int(line[0])))

	print('Loading answers...')
	with open(ANSWERS_FILE) as csv_answers:
		readCSV = csv.reader(csv_answers, delimiter=';')
		next(readCSV)
		for line in readCSV:
			answers.append(line[1].rstrip())


# I DONT BELIEVE YOU, we need to answer that


def init_text_parser():
	global bert_client
	bert_client = BertClient(port=5555, port_out=5556)
	load_questions()

def main():
	init_chatbot()
	init_text_parser()
	tel_updater.start_polling(bootstrap_retries=0)


if __name__ == '__main__':
	main()
