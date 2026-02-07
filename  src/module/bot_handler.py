import os
import time


class HabrBotHandler:
    def __init__(self, bot, tg_id, post_parser, sleep_seconds=600):
        self.bot = bot
        self.tg_id = tg_id
        self.post_parser = post_parser
        self.sleep_seconds = sleep_seconds

    def register_handlers(self):
        @self.bot.message_handler(content_types=['text'])
        def __commands(message):
            if message.text == "Старт":
                back_post_id = None
                while True:
                    post_text, back_post_id = self.post_parser.parse_new_post(back_post_id)

                    if post_text is not None:
                        if os.path.isdir('../../image') and os.listdir('../../image'):
                            with open(f'image/{back_post_id}.png', 'rb') as photo:
                                self.bot.send_photo(
                                    self.tg_id,
                                    photo=photo,
                                    caption=post_text,
                                    parse_mode='HTML',
                                )
                                os.remove(f'image/{back_post_id}.png')
                        else:
                            self.bot.send_message(self.tg_id, post_text, parse_mode='HTML')
                    time.sleep(self.sleep_seconds)
            else:
                self.bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")