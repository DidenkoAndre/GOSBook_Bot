# -*- coding: utf-8 -*-
import logging
from telegram.ext import CommandHandler, Updater
from telegram import Document, Bot, Chat
from telegram.error import NetworkError, Unauthorized, TelegramError
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from functools import wraps

LIST_OF_ADMINS = []
with open('admin_ids', 'r') as admins:
    for chat_id in admins.read().splitlines():
        LIST_OF_ADMINS.append(int(chat_id))

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.message.chat_id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

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

def add_starter(chat_id):
    with open('starters.txt', 'a') as db:
        db.write(str(chat_id) + '\n')
    return None

def get_starters():
    with open('starters.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for id in ids:
        res.append(int(id))
    return res

@restricted
def get_numberofstarters(bot, update):
	id = update.message.chat_id
	bot.sendMessage(chat_id = id, text = "Количество стартеров у этого бота: " + str(len(get_starters())))

@restricted
def get_users_starters(bot, update):
	id = update.message.chat_id
	sub_list = []
	for sub in get_starters():
		chat = bot.getChat(sub)
		if chat.type == 'private':
			sub_list.append(chat.first_name + ' ' + chat.last_name)
		else:
			sub_list.append("Группа: " + chat.title)
	message = '\n'.join(sub_list)
	bot.sendMessage(chat_id = id, text = 'Список стартеров:\n'+message)

def start(bot, update):
	id = update.message.chat_id
	if id not in get_starters():
		add_starter(id)
        bot.sendMessage(chat_id=update.message.chat_id, text = "Я бот, вижу, вы хотите поботать ГОС?\n\
	Для ознакомления со списком возможных команд, запросите /help")

def help(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text = '''**Список команд данного бота:**\n
	/book -- получить последнюю версию ГОСБука в pdf-формате\n
	/subscribe -- подписаться на рассылку об обновлениях ГОСБука, чтобы автоматически получать новые версии ГОСБука, а также читать новости, касающиеся ГОСа\n
	/unsubscribe -- отписаться от выше указанной новостной рассылки\n
	/help -- вывести список команд данного бота\n\n
	PS. Если я как-то неправильно работаю или у тебя есть интересные предложения по улучшению меня, то напиши, пожалуйста, моему создателю @didenko_andre''')

def getbook(bot, update):
	id = update.message.chat_id
	if id not in get_starters():
		add_starter(id)
        send_file(bot, "/home/ec2-user/GOS_book/GOSBook Matan.pdf", id, None,
                      caption="Вот последняя версия ГОСбука")


### SUBSRIBE RELATED FUNCTIONS

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

def unsubscribe(bot, update):
    id = update.message.chat_id
    if id not in get_subscribers():
        bot.sendMessage(chat_id=id, text = "Вы не являетесь подписчиком!")
        return None
    del_subscriber(id)
    bot.sendMessage(chat_id=id, text = "Вы прекратили свою подписку на рассылку об обновлениях ГОСбука!")

### TEST SUBSS RELATED FUNCTIONS

def get_testsubs():
    with open('testsubs.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for id in ids:
        res.append(int(id))
    return res

def add_testsub(chat_id):
    with open('testsubs.txt', 'a') as db:
        db.write(str(chat_id) + '\n')
    return None

def del_testsubs(chat_id):
    with open('testsubs.txt', 'r') as db:
        testsubs = db.read().splitlines()
        testsubs.remove(str(chat_id))
    with open('testsubs.txt', 'w') as db:
        db.write('\n'.join(testsubs)+'\n')
    return None

def testsubscribe(bot, update):
    id = update.message.chat_id
    if id in get_testsubs():
        bot.sendMessage(chat_id=id, text = "Вы уже являетесь БЕТА-тестером!")
        return None
    add_testsub(id)
    bot.sendMessage(chat_id=id, text = "Вы успешно подписались на ТЕСТОВУЮ рассылку!")

def testunsubscribe(bot, update):
    id = update.message.chat_id
    if id not in get_testsubs():
        bot.sendMessage(chat_id=id, text = "Вы не являетесь БЕТА-тестером!")
        return None
    del_testsub(id)
    bot.sendMessage(chat_id=id, text = "Вы прекратили свою подписку на ТЕСТОВУЮ рассылку!")


@restricted
def get_numberofsubs(bot, update):
	id = update.message.chat_id
	bot.sendMessage(chat_id = id, text = "Количество подписчиков у этого бота: " + str(len(get_subscribers())))

@restricted
def get_users(bot, update):
	id = update.message.chat_id
	sub_list = []
	for sub in get_subscribers():
		chat = bot.getChat(sub)
		if chat.type == 'private':
			sub_list.append(chat.first_name + ' ' + chat.last_name)
		else:
			sub_list.append("Группа: " + chat.title)
	message = '\n'.join(sub_list)
	bot.sendMessage(chat_id = id, text = 'Список подписчиков:\n'+message)


@restricted
def get_numberoftestsubs(bot, update):
	id = update.message.chat_id
	bot.sendMessage(chat_id = id, text = "Количество БЕТА-тестеров у этого бота: " + str(len(get_testsubs())))

@restricted
def get_testusers(bot, update):
	id = update.message.chat_id
	sub_list = []
	for sub in get_testsubs():
		chat = bot.getChat(sub)
		if chat.type == 'private':
			sub_list.append(chat.first_name + ' ' + chat.last_name)
		else:
			sub_list.append("Группа: " + chat.title)
	message = '\n'.join(sub_list)
	bot.sendMessage(chat_id = id, text = 'Список БЕТА-тестеров:\n'+message)

def get_suspects():
    with open('suspects.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for id in ids:
        res.append(int(id))
    return res

@restricted
def get_suspectusers(bot, update):
	id = update.message.chat_id
	sub_list = []
	for sub in get_suspects():
		chat = bot.getChat(sub)
		if chat.type == 'private':
			sub_list.append(chat.first_name + ' ' + chat.last_name)
		else:
			sub_list.append("Группа: " + chat.title)
	sub_list = list(set(sub_list))
	message = '\n'.join(sub_list)
	bot.sendMessage(chat_id = id, text = 'Список подозреваемых:\n'+message)

@restricted
def saytopeople(bot, update):
	message = update.message.text
	message = message.split("\n",2)[2];
	for id in get_subscribers():
		chat = bot.getChat(id)
   		prefix = ''
   		if chat.type == 'private':
      	 		prefix = 'Дорогой(-ая) ' + chat.first_name + '!\n'
		try:    
    			bot.sendMessage(chat_id=id, text = message)
		except TelegramError as err:
			check_suspect(id)
		time.sleep(1)

@restricted
def secretinfo(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text = '''**Список секретных команд данного бота:**\n
/howmuch -- узнать количество подписчиков данного бота\n
/show_subs -- показать список подписчиков\n
/howmanystar -- узнать количество стартеров\n
/show_starters -- вывести список стартеров\n
/show_suspects -- вывести список подозреваемых\n
\n
/testsubscribe -- стать БЕТА-тестером\n
/testunsubscribe -- перестать быть БЕТА-тестером\n
/howmanytest -- узнать количество БЕТА-тестеров\n
/show_testsubs -- показать БЕТА-тестеров\n
\n
/saytopeople -- начни сообщение с двух новых строк и оно будет бродкастено по подписчикам''')

if __name__ == '__main__':
	with open('GOSBook_Bot_token', 'r') as file1:
		TOKEN = file1.read().strip()

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

	testsubscribe_handler = CommandHandler('testsubscribe',testsubscribe)
	dispatcher.add_handler(testsubscribe_handler)
	testunsubscribe_handler = CommandHandler('testunsubscribe',testunsubscribe)
	dispatcher.add_handler(testunsubscribe_handler)	

	# restricted commands
	howmuch_handler = CommandHandler('howmuch', get_numberofsubs)
	dispatcher.add_handler(howmuch_handler)
	users_handler = CommandHandler('show_subs', get_users)
	dispatcher.add_handler(users_handler)
	suspectusers_handler = CommandHandler('show_suspects', get_suspectusers)
	dispatcher.add_handler(suspectusers_handler)
	howmanystar_handler = CommandHandler('howmanystar', get_numberofstarters)
	dispatcher.add_handler(howmanystar_handler)
	starters_handler = CommandHandler('show_starters', get_users_starters)
	dispatcher.add_handler(starters_handler)
	howmanytest_handler = CommandHandler('howmanytest', get_numberoftestsubs)
	dispatcher.add_handler(howmanytest_handler)
	testusers_handler = CommandHandler('show_testsubs', get_testusers)
	dispatcher.add_handler(testusers_handler)
	secretinfo_handler = CommandHandler('secretinfo', secretinfo)
	dispatcher.add_handler(secretinfo_handler)
        saytopeople_handler = CommandHandler('saytopeople', saytopeople)
        dispatcher.add_handler(saytopeople_handler)


	updater.start_polling()
	updater.idle()
