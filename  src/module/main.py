import os
import telebot
from dotenv import load_dotenv
from ParserHabr import Parser


class BotApplication:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.tg_id = os.getenv('CHANNEL_ID')
        self.bot = telebot.TeleBot(self.token)
        self.parser = Parser(self.bot, self.tg_id)

    def run(self):
        self.parser.firstMessage()
        self.bot.polling(none_stop=True, timeout=20)


if __name__ == '__main__':
    BotApplication().run()
