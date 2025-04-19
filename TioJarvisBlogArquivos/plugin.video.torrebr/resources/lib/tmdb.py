import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import requests
from urllib.parse import urlencode, quote
from resources.lib.utils import logger, get_icon

class TMDbAPI:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_URL = "https://image.tmdb.org/t/p/w500"

    def __init__(self, handle):
        self.handle = handle
        self.addon = xbmcaddon.Addon()
        self.api_key = self.addon.getSettingString('tmdb_api_key')
        self.language = 'pt-BR'
        self.session = requests.Session()

    def _get(self, endpoint, params=None):
        params = params or {}
        params.update({'api_key': self.api_key, 'language': self.language})
        try:
            response = self.session.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger(f"Erro na API TMDb: {str(e)}", xbmc.LOGERROR)
            return None

    def list_popular_movies(self):
        data = self._get("/movie/popular")
        if data and 'results' in data:
            for movie in data['results']:
                self._add_movie_item(movie)

    def list_popular_series(self):
        data = self._get("/tv/popular")
        if data and 'results' in data:
            for series in data['results']:
                self._add_series_item(series)

    def search_content(self, query):
        data_movies = self._get("/search/movie", {'query': query})
        data_tv = self._get("/search/tv", {'query': query})
        if data_movies and 'results' in data_movies:
            for item in data_movies['results']:
                self._add_movie_item(item)
        if data_tv and 'results' in data_tv:
            for item in data_tv['results']:
                self._add_series_item(item)

    def _add_movie_item(self, movie):
        title = movie.get('title', 'Sem título')
        poster = f"{self.IMAGE_URL}{movie['poster_path']}" if movie.get('poster_path') else get_icon('default_poster.png')
        li = xbmcgui.ListItem(label=title)
        li.setArt({'poster': poster, 'fanart': f"{self.IMAGE_URL}{movie['backdrop_path']}" if movie.get('backdrop_path') else ''})
        li.setInfo('video', {'plot': movie.get('overview', ''), 'year': movie.get('release_date', '')[:4]})
        url = f"{sys.argv[0]}?action=search_torrents&title={quote(title)}"
        xbmcplugin.addDirectoryItem(self.handle, url, li, True)

    def _add_series_item(self, series):
        title = series.get('name', 'Sem título')
        poster = f"{self.IMAGE_URL}{series['poster_path']}" if series.get('poster_path') else get_icon('default_poster.png')
        li = xbmcgui.ListItem(label=title)
        li.setArt({'poster': poster, 'fanart': f"{self.IMAGE_URL}{series['backdrop_path']}" if series.get('backdrop_path') else ''})
        li.setInfo('video', {'plot': series.get('overview', ''), 'year': series.get('first_air_date', '')[:4]})
        url = f"{sys.argv[0]}?action=search_torrents&title={quote(title)}"
        xbmcplugin.addDirectoryItem(self.handle, url, li, True)
