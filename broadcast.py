# -*- coding: utf-8 -*-
from bot import send_file, get_subscribers, get_suspects, check_suspect, get_testsubs
from telegram import Document, Bot
from telegram.error import TelegramError
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('GOSBook_Bot_token', 'r') as file:
	TOKEN = file.read().strip()
	
bot = Bot(token = TOKEN)
message = sys.argv[1]

time.sleep(60)
for id in get_subsribers():
	chat = bot.getChat(id)
   	prefix = ''
   	if chat.type == 'private':
       		prefix = 'Дорогой(-ая) ' + chat.first_name + '!\n'
	try:    
		send_file(bot, "/home/ec2-user/GOS_book/GOSBook_Matan.pdf", id, None, caption=prefix+"Вышла новая версия ГОСбука.")
    		bot.sendMessage(chat_id=id, text = message)
	except TelegramError as err:
		check_suspect(id)
	time.sleep(1)
