# -*- coding: utf-8 -*-
import logging
from telegram.ext import CommandHandler, Updater
from telegram import Document, Bot
from telegram.error import NetworkError, Unauthorized, TelegramError
import time

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

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text = "Я бот, вижу, вы хотите поботать ГОС?\n\
	Для ознакомления со списком возможных команд, запросите /help")
	
def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text = "Список команд данного бота:\n\
	/book -- получить последнюю версию ГОСБука в pdf-формате\n\
	/subscribe -- подписаться на рассылку об обновлениях ГОСБука, чтобы автоматически получать новые версии ГОСБука, а также читать новости, касающиеся ГОСа\n\
	/unsubscribe -- отписаться от выше указанной новостной рассылки\n\
	/help -- вывести список команд данного бота\n\n\
	PS. Если я как-то неправильно работаю или у тебя есть интересные предложения по улучшению меня, то напиши, пожалуйста, моему создателю @didenko_andre")

def getbook(bot, update):
    send_file(bot, "/home/ec2-user/GOS_book/GOSBook.pdf", update.message.chat_id, None,
                      caption="Вот последняя версия ГОСбука")

def get_subscribers():
    with open('subscribers.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for id in ids:
        res.append(int(id))
    return res

def add_subscriber(chat_id):
    with open('subscribers.txt', 'a') as db:
        db.write(str(chat_id) + '\n')
    return None

def del_subscriber(chat_id):
    with open('subscribers.txt', 'r') as db:
        subscribers = db.read().splitlines()
        subscribers.remove(str(chat_id))
    with open('subscribers.txt', 'w') as db:
        db.write('\n'.join(subscribers)+'\n')
    return None

def subscribe(bot, update):
    id = update.message.chat_id
    if id in get_subscribers():
        bot.sendMessage(chat_id=id, text = "Вы уже являетесь подписчиком!")
        return None
    add_subscriber(id)	
    bot.sendMessage(chat_id=id, text = "Вы успешно подписались на рассылку об обновлениях ГОСбука!")
	
	bot.sendMessage(chat_id=didenko_andre_id, text = \
	"На твоего бота подписался еще один человек, теперь у бота " + str(len(get_subscribers())) + "подписчиков.")

def unsubscribe(bot, update):
    id = update.message.chat_id
    if id not in get_subscribers():
        bot.sendMessage(chat_id=id, text = "Вы не являетесь подписчиком!")
        return None
    del_subscriber(id)
    bot.sendMessage(chat_id=id, text = "Вы прекратили свою подписку на рассылку об обновлениях ГОСбука!")
	
	bot.sendMessage(chat_id=didenko_andre_id, text = \
	"От твоего бота кто-то отписался, теперь у бота " + str(len(get_subscribers())) + "подписчиков.")

if __name__ == '__main__':
	with open('GOSBook_Bot_token') as file1:
		TOKEN = file.read().strip()
		
	with open('didenko_andre_id') as file2:
		didenko_andre_id = file.read().strip()
	
	updater = Updater(token = TOKEN)
	dispatcher = updater.dispatcher

	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    level=logging.INFO)
	# Command handlers
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)
	help_handler = CommandHandler('help', help)
	dispatcher.add_handler(help_handler)
	book_handler = CommandHandler('book', getbook)
	dispatcher.add_handler(book_handler)
	subscribe_handler = CommandHandler('subscribe',subscribe)
	dispatcher.add_handler(subscribe_handler)
	unsubscribe_handler = CommandHandler('unsubscribe',unsubscribe)
	dispatcher.add_handler(unsubscribe_handler)

	updater.start_polling()
	print "Hello WOrld"

	updater.idle()
