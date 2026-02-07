import os
import requests


class ImageDownloader:
    def __init__(self, images_dir='../../image', local_dir='image'):
        self.images_dir = images_dir
        self.local_dir = local_dir

    def download(self, post_id, img_url):
        os.makedirs(self.images_dir, exist_ok=True)
        file_path = f'{self.local_dir}/{post_id}.png'
        with requests.get(img_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return file_path