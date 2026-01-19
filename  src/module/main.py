import telebot
import os
from dotenv import load_dotenv
from ParserHabr import Parser

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
TG = os.getenv('CHANNEL_ID')

bot = telebot.TeleBot(TOKEN)

parser = Parser(bot, TG)

if __name__ == '__main__':
    parser.firstMessage()
    bot.polling(none_stop=True, timeout=20)