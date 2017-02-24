# -*- coding: utf-8 -*-
from bot import send_file, get_subscribers
from telegram import Document, Bot
from telegram.error import NetworkError, Unauthorized, TelegramError
import time

with open('GOSBook_Bot_token') as file:
	TOKEN = file.read().strip()
	
bot = Bot(token = TOKEN)

for id in get_subscribers():
    send_file(bot, "/home/ec2-user/GOS_book/GOSBook.pdf", id, None, caption="Вышла новая версия ГОСбука! Получайте свежую версию книги.")
    time.sleep(1)
