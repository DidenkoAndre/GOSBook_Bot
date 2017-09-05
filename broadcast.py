# -*- coding: utf-8 -*-
from bot import send_file, get_subscribers
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


def get_suspects():
    with open('suspects.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for id in ids:
        res.append(int(id))
    return res

def check_suspect(suspect_id):    
    with open('suspects.txt', 'r') as db:
        suspects = db.read().splitlines()
        suspects.append(str(suspect_id))
        if ((sum(1 for i in get_suspects() if i == suspect_id)) > 5):
        	suspects = [id for id in suspects if id != str(suspect_id)]
		del_subscriber(suspect_id)
    with open('suspects.txt', 'w') as db:
        db.write('\n'.join(suspects[-100:])+'\n')
    return None


time.sleep(60)
for id in get_subscribers():
	chat = bot.getChat(id)
   	prefix = ''
   	if chat.type == 'private':
       		prefix = 'Дорогой(-ая) ' + chat.first_name + '!\n'
	try:    
		send_file(bot, "/home/ec2-user/GOS_book/GOSBook Matan.pdf", id, None, caption=prefix+"Вышла новая версия ГОСбука.")
    		bot.sendMessage(chat_id=id, text = message)
	except TelegramError as err:
		check_suspect(id)
	time.sleep(1)
