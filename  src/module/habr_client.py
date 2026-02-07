import requests
from bs4 import BeautifulSoup


class HabrFeedClient:
    def __init__(self, url="https://habr.com/ru/feed/"):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_latest_post(self):
        page = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(page.content, "lxml")
        post = soup.find("article", class_="tm-articles-list__item", id=True)
        post_id = post["id"]
        return post_id, post, soup