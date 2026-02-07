class HabrPostParser:
    def __init__(self, feed_client, image_downloader):
        self.feed_client = feed_client
        self.image_downloader = image_downloader

    def parse_new_post(self, back_post_id):
        post_id, post, soup = self.feed_client.fetch_latest_post()
        if post_id != back_post_id:
            title = post.find("a", class_="tm-title__link").text.strip()
            description = soup.find(
                "div",
                class_=(
                    "article-formatted-body article-formatted-body "
                    "article-formatted-body_version-2"
                ),
            ).text.strip()
            url = post.find("a", class_="tm-title__link", href=True)["href"].strip()
            img = post.find('img', class_='lead-image')
            if not img:
                return None, post_id
            img_url = img.get('src')
            self.image_downloader.download(post_id, img_url)
            return (
                f"<b>{title}</b>\n\n{description}\n\n"
                f"<a href='https://habr.com{url}'><b>Ссылка на статью</b></a>",
                post_id,
            )
        return None, post_id