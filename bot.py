# -*- coding: utf-8 -*-

from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram import Document, File, Bot
from telegram.error import NetworkError, Unauthorized, TelegramError

import time

TOKEN = '305103696:AAGtt_a0EjkvU7F9ySpi1Snn6eHkMgWRW0U'
updater = Updater(token = TOKEN)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.INFO)

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text = "Я бот, вижу, вы хотите поботать ГОС?")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
	

def send_file(bot, filename, chat_id, _type, caption, **kwargs):

    def upload(file_id):
		v = bot.sendDocument(bot=bot, document=open(filename, 'r'), chat_id=chat_id, caption=caption)
		return v
    try:
        return upload(str(hash(filename)))
    except TelegramError as e:
        if "file_id" in e.message:
            return upload("s")
        else:
            raise e

    return upload_from_disk()

	
def getbook(bot, update):
	send_file(bot, "_main.pdf", update.message.chat_id, None,
                      caption="Вот ваша книга")
					  
subscribe_list = open("subscribelist.txt").read().splitlines()

def subscribe(bot, update):
	id = update.message.chat_id
	if id in subscribe_list:
		bot.sendMessage(chat_id=id, text = "Вы уже являетесь подписчиком!")
		return None	
	
	thefile = open('subscribelist.txt', 'w')
	thefile.write("%s\n" % id)
	
	bot.sendMessage(chat_id=id, text = "Вы успешно подписались на рассылку о обновлениях ГОСбука!")
	print subscribe_list
	thefile.close()
	
def unsubscribe(bot, update):
	id = update.message.chat_id
	if id not in subscribe_list:
		bot.sendMessage(chat_id=id, text = "Вы не являетесь подписчиком!")
		return None
		
	thefile = open('subscribelist.txt', 'rw')
	lines = thefile.readlines()
	for line in lines:
		if line != str(id) + "\n":
			thefile.write(line)
			
	thefile.close()
	
	bot.sendMessage(chat_id=id, text = "Вы прекратили свою подписку о обновлениях ГОСбука!")

book_handler = CommandHandler('book', getbook)
dispatcher.add_handler(book_handler)

subscribe_handler = CommandHandler('subscribe',subscribe)
dispatcher.add_handler(subscribe_handler)

unsubscribe_handler = CommandHandler('unsubscribe',unsubscribe)
dispatcher.add_handler(unsubscribe_handler)

updater.start_polling()
print "Hello WOrld"

bot = Bot(token=TOKEN)
while True:
	for id in subscribe_list:
		bot.sendMessage(chat_id = id, text = "Привет, подписота")
		time.sleep(1)


updater.idle()