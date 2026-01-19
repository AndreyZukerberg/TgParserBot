import time
from bs4 import BeautifulSoup
import requests
import os

class Parser:
    def __init__(self, bot, TG):
        self.bot = bot
        self.TG = TG

    def requestId(self):
        url = "https://habr.com/ru/feed/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")

        post = soup.find("article", class_="tm-articles-list__item", id=True)
        post_id = post["id"]
        return post_id, post, soup

    def parserSoup(self, back_post_id):
        ReqID = self.requestId()
        if ReqID[0] != back_post_id:
            title = ReqID[1].find("a", class_="tm-title__link").text.strip()
            description = ReqID[2].find("div", class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text.strip()
            url = ReqID[1].find("a", class_="tm-title__link", href=True)["href"].strip()
            # функция отвечает за скачивание фотографии
            img = ReqID[1].find('img', class_='lead-image')
            if not img:
                return None, ReqID[0]
            img_url = img.get('src')
            """↓ Скачивание изображений с постов ↓"""
            os.makedirs('../../image', exist_ok=True)
            with requests.get(img_url, stream=True) as r:
                r.raise_for_status()
                with open('image/' + f'{ReqID[0]}.png', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            return f"<b>{title}</b>\n\n{description}\n\n<a href='https://habr.com{url}'><b>Ссылка на статью</b></a>", ReqID[0]
        else:
            return None, ReqID[0]

    def firstMessage(self):
        @self.bot.message_handler(content_types=['text'])
        def __commands(message):
            if message.text == "Старт":
                back_post_id = None
                while True:
                    post_text = self.parserSoup(back_post_id)
                    back_post_id = post_text[1]

                    if post_text[0] is not None:
                        if os.path.isdir('../../image') and os.listdir('../../image'):
                            with open('image/' + post_text[1] + '.png', 'rb') as photo:
                                self.bot.send_photo(self.TG, photo=photo, caption=post_text[0], parse_mode='HTML')
                                os.remove('image/' + post_text[1] + '.png')
                        else:
                            self.bot.send_message(self.TG, post_text[0], parse_mode='HTML')
                    time.sleep(600)
            else:
                self.bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")

