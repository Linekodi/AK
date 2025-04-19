import re
import time
import requests
import xbmcgui
from urllib.parse import quote
from resources.lib.utils import logger

class TorrentProviders:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search_torrents(self, title, media_type='movie'):
        """Busca torrents em múltiplos provedores públicos"""
        results = []
        query = quote(title)

        # YTS (API)
        try:
            results += self._yts_api(query)
        except Exception as e:
            logger(f"Erro no YTS: {str(e)}", xbmc.LOGERROR)

        # RARBG (API)
        try:
            results += self._rarbg_api(query, media_type)
        except Exception as e:
            logger(f"Erro no RARBG: {str(e)}", xbmc.LOGERROR)

        # 1337x (Scraping simplificado)
        try:
            results += self._1337x_scrape(query)
        except Exception as e:
            logger(f"Erro no 1337x: {str(e)}", xbmc.LOGERROR)

        # Ordena por seeders (maior primeiro)
        return sorted(results, key=lambda x: x.get('seeders', 0), reverse=True)

    # ==================== YTS (API Oficial) ====================
    def _yts_api(self, query):
        url = f"https://yts.mx/api/v2/list_movies.json?query_term={query}&sort_by=seeds"
        response = self.session.get(url, headers=self.headers, timeout=10)
        data = response.json()

        torrents = []
        for movie in data.get('data', {}).get('movies', []):
            for torrent in movie.get('torrents', []):
                torrents.append({
                    'name': f"{movie['title']} [YTS] [Quality: {torrent['quality']}]",
                    'size': torrent['size'],
                    'seeders': torrent['seeds'],
                    'magnet': self._convert_to_magnet(torrent['hash']),
                    'provider': 'YTS'
                })
        return torrents

    # ==================== RARBG (API com Token) ====================
    def _rarbg_api(self, query, media_type):
        token = self._get_rarbg_token()
        if not token:
            return []

        # Tipos de conteúdo compatíveis
        category = {
            'movie': 'movies',
            'series': 'tv'
        }.get(media_type, 'movies')

        url = f"https://torrentapi.org/pubapi_v2.php?mode=search&search_string={query}&category=44;18&sort=seeders&format=json_extended&token={token}"
        time.sleep(2)  # Limite de 1 requisição/2s
        response = self.session.get(url, headers=self.headers, timeout=15)
        data = response.json()

        torrents = []
        for item in data.get('torrent_results', []):
            torrents.append({
                'name': f"{item['title']} [RARBG]",
                'size': f"{round(item['size'] / (1024**3), 1)} GB",
                'seeders': item['seeders'],
                'magnet': item['download'],
                'provider': 'RARBG'
            })
        return torrents

    def _get_rarbg_token(self):
        try:
            response = self.session.get(
                "https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=TorreBR",
                headers=self.headers,
                timeout=10
            )
            return response.json().get('token')
        except:
            return None

    # ==================== 1337x (Scraping Básico) ====================
    def _1337x_scrape(self, query):
        url = f"https://www.1337x.to/search/{query}/1/"
        response = self.session.get(url, headers=self.headers, timeout=15)
        html = response.text

        # Extrai magnet links via regex (simplificado)
        magnets = re.findall(r'href="(magnet:\?[^"]+)"', html)
        names = re.findall(r'class="name">([^<]+)<', html)[:10]  # Limita a 10 resultados

        torrents = []
        for name, magnet in zip(names, magnets):
            torrents.append({
                'name': f"{name} [1337x]",
                'size': 'N/A',
                'seeders': 0,
                'magnet': magnet,
                'provider': '1337x'
            })
        return torrents

    @staticmethod
    def _convert_to_magnet(hash):
        return f'magnet:?xt=urn:btih:{hash}&dn=YTS+Torrent'
