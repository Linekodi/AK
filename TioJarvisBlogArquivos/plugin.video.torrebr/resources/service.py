import xbmc
import xbmcaddon
import threading
from time import sleep
from resources.lib.tmdb import TMDbAPI
from resources.lib.debrid import RealDebrid
from resources.lib.utils import logger

class BackgroundService(threading.Thread):
    def __init__(self):
        super(BackgroundService, self).__init__()
        self.addon = xbmcaddon.Addon()
        self._stop_event = threading.Event()
        self.update_interval = 3600  # 1 hora

    def run(self):
        logger("Serviço em segundo plano iniciado")
        while not self._stop_event.is_set():
            try:
                if self.addon.getSettingBool('enable_auto_update'):
                    self.update_tmdb_cache()
                self.check_debrid_token()
            except Exception as e:
                logger(f"Erro no serviço: {str(e)}", xbmc.LOGERROR)
            sleep(self.update_interval)

    def update_tmdb_cache(self):
        logger("Atualizando cache do TMDb...")
        tmdb = TMDbAPI(-1)  # Handle inválido para background
        tmdb.list_popular_movies()
        tmdb.list_popular_series()

    def check_debrid_token(self):
        token = self.addon.getSettingString('realdebrid_token')
        if token:
            try:
                debrid = RealDebrid(token)
                if not debrid.resolve_magnet("magnet:?xt=urn:btih:TEST"):
                    logger("Token Real-Debrid inválido!", xbmc.LOGWARNING)
            except:
                pass

    def stop(self):
        self._stop_event.set()
        logger("Serviço em segundo plano parado")

if __name__ == '__main__':
    service = BackgroundService()
    service.start()
