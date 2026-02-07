from bot_handler import HabrBotHandler
from habr_client import HabrFeedClient
from image_downloader import ImageDownloader
from post_parser import HabrPostParser


class Parser:
    def __init__(self, bot, tg_id):
        self.bot = bot
        self.tg_id = tg_id
        self.feed_client = HabrFeedClient()
        self.image_downloader = ImageDownloader()
        self.post_parser = HabrPostParser(self.feed_client, self.image_downloader)
        self.bot_handler = HabrBotHandler(self.bot, self.tg_id, self.post_parser)

    def requestId(self):
        return self.feed_client.fetch_latest_post()

    def parserSoup(self, back_post_id):
        return self.post_parser.parse_new_post(back_post_id)

    def firstMessage(self):
        self.bot_handler.register_handlers()