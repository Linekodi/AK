from .scraper import Scraper
from .player import Player

class Realhub:
    def __init__(self):
        self.scraper = Scraper()
        self.player = Player()

    def list_videos(self, category_url):
        videos = self.scraper.get_videos(category_url)
        for video in videos:
            # Imprimir informações de vídeo aqui
            print(video.title)
            print(video.url)
            print(video.image_url)
        # Restante do código aqui
