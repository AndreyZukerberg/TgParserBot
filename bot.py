import time
import telebot
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
TG = os.getenv('CHANNEL_ID')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def commands(message):
    if message.text == "Старт":
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(TG, post_text[0], parse_mode='HTML')
                time.sleep(1800)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")

def parser(back_post_id):
    URL = "https://habr.com/ru/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    post = soup.find("article", class_="tm-articles-list__item", id=True)
    post_id = post["id"]

    if post_id != back_post_id:
        title = post.find("a", class_="tm-title__link").text.strip()
        description = soup.find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
        url = post.find("a", class_="tm-title__link", href=True)["href"].strip()
        """img = post.find("img", class_="lead-image")["src"].strip"""

        return f"'<b>'{title}'</b>'\n\n{description}\n\nhttps://habr.com{url}", post_id
    else:
        return None, post_id


bot.polling()