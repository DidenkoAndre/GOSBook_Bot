# -*- coding: utf-8 -*-
from bot import send_file, get_subscribers
from telegram import Document, Bot
from telegram.error import NetworkError, Unauthorized, TelegramError
import time

TOKEN = '305103696:AAGtt_a0EjkvU7F9ySpi1Snn6eHkMgWRW0U'
bot = Bot(token = TOKEN)

for id in get_subscribers():
    send_file(bot, "/home/ec2-user/GOS_book/_main.pdf", id, None, caption="Вышла новая версия ГОСбука! Получайте свежую версию книги.")
    time.sleep(1)
