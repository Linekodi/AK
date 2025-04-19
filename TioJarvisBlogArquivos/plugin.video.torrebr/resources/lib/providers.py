import re
import xbmc
import requests
from urllib.parse import quote, unquote
from resources.lib.utils import logger

class TorrentProviders:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.timeout = 30
        self.retries = 2   # Número de tentativas

    def search_torrents(self, title, media_type='movie'):
        results = []
        query = quote(title)

        # Novos provedores
        results += self._bludv(query)
        results += self._filmestorrenttv(query)
        results += self._filmetorrent(query)
        results += self._torrentplus(query)

        return sorted(results, key=lambda x: x.get('seeders', 0), reverse=True)

    # ==================== BluDV ====================
    def _bludv(self, query):
        try:
            url = f"https://bludv.xyz/?s={query}"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            html = response.text

            pattern = r'<article.*?href="(https://bludv.xyz/[^"]+)".*?<h2 class="entry-title">([^<]+)</h2>.*?<span class="size">([^<]+)</span>'
            matches = re.findall(pattern, html, re.DOTALL)

            return [{
                'name': unquote(match[1].strip()),
                'magnet': self._extract_bludv_magnet(match[0]),
                'size': match[2].strip(),
                'provider': 'BluDV',
                'seeders': 100  # Valor padrão
            } for match in matches[:10]]
        except Exception as e:
            logger(f"Erro no BluDV: {str(e)}", xbmc.LOGERROR)
            return []

    def _extract_bludv_magnet(self, url):
        try:
            response = self.session.get(url, timeout=self.timeout)
            return re.search(r'href="(magnet:\?[^"]+)"', response.text).group(1)
        except:
            return ''

    # ==================== Filmes Torrent TV ====================
    def _filmestorrenttv(self, query):
        try:
            url = f"https://filmestorrenttv.net/?s={query}"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            html = response.text

            pattern = r'<div class="item">.*?href="([^"]+)".*?<span class="ttx">([^<]+)</span>.*?<span class="calidad2">([^<]+)</span>'
            matches = re.findall(pattern, html, re.DOTALL)

            return [{
                'name': f"{unquote(match[1])} [{match[2]}]",
                'magnet': self._extract_generic_magnet(match[0]),
                'size': 'N/A',
                'provider': 'FilmesTorrentTV',
                'seeders': 50
            } for match in matches[:8]]
        except Exception as e:
            logger(f"Erro no FilmesTorrentTV: {str(e)}", xbmc.LOGERROR)
            return []

    # ==================== Filme Torrent ====================
    def _filmetorrent(self, query):
        try:
            url = f"https://filmetorrent.org/?s={query}"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            html = response.text

            pattern = r'<div class="post">.*?href="([^"]+)".*?<h2>([^<]+)</h2>.*?<span>Size:</span>([^<]+)<'
            matches = re.findall(pattern, html, re.DOTALL)

            return [{
                'name': unquote(match[1].strip()),
                'magnet': self._extract_generic_magnet(match[0]),
                'size': match[2].strip(),
                'provider': 'FilmeTorrent',
                'seeders': 75
            } for match in matches[:10]]
        except Exception as e:
            logger(f"Erro no FilmeTorrent: {str(e)}", xbmc.LOGERROR)
            return []

    # ==================== TorrentPlus ====================
    def _torrentplus(self, query):
        try:
            url = f"https://torrentplus.org/?s={query}"
            response = self.session.get(url, headers=self.headers, timeout=self.timeout)
            html = response.text

            pattern = r'<li class="list-item">.*?href="([^"]+)".*?<h3>([^<]+)</h3>.*?<span class="size">([^<]+)</span>'
            matches = re.findall(pattern, html, re.DOTALL)

            return [{
                'name': unquote(match[1].strip()),
                'magnet': self._extract_generic_magnet(match[0]),
                'size': match[2].strip(),
                'provider': 'TorrentPlus',
                'seeders': self._parse_seeders(match[1])
            } for match in matches[:12]]
        except Exception as e:
            logger(f"Erro no TorrentPlus: {str(e)}", xbmc.LOGERROR)
            return []

    def _extract_generic_magnet(self, url):
        try:
            response = self.session.get(url, timeout=self.timeout)
            magnet = re.search(r'href="(magnet:\?[^"]+)"', response.text)
            return magnet.group(1) if magnet else ''
        except:
            return ''

    def _parse_seeders(self, title):
        if any(s in title.lower() for s in ['4k', '2160p']):
            return 150
        elif any(s in title.lower() for s in ['1080p', 'fhd']):
            return 100
        else:
            return 50
