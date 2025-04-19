import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon  # Importação adicionada
import requests
from urllib.parse import urlencode
from resources.lib.utils import logger, get_icon

class TMDbAPI:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_URL = "https://image.tmdb.org/t/p/w500"

    def __init__(self, handle):
        self.handle = handle  # Recebe HANDLE do default.py
        self.addon = xbmcaddon.Addon()
        self.api_key = self.addon.getSettingString('tmdb_api_key')
        self.session = requests.Session()

    # ... (métodos _get, list_popular_movies, list_popular_series iguais) ...

    def _add_movie_item(self, movie):
        title = movie.get('title', 'Sem título')
        poster = f"{self.IMAGE_URL}{movie['poster_path']}" if movie.get('poster_path') else get_icon('default_poster.png')

        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({
            'poster': poster,
            'fanart': f"{self.IMAGE_URL}{movie['backdrop_path']}" if movie.get('backdrop_path') else ''
        })
        list_item.setInfo('video', {
            'plot': movie.get('overview', ''),
            'year': movie.get('release_date', '')[:4]
        })

        url = f"{sys.argv[0]}?action=resolve_torrent&magnet={movie['id']}"
        xbmcplugin.addDirectoryItem(
            handle=self.handle,  # Usa self.handle
            url=url,
            listitem=list_item,
            isFolder=False
        )

    def _add_series_item(self, series):  # Implementação completa
        title = series.get('name', 'Sem título')
        poster = f"{self.IMAGE_URL}{series['poster_path']}" if series.get('poster_path') else get_icon('default_poster.png')

        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({
            'poster': poster,
            'fanart': f"{self.IMAGE_URL}{series['backdrop_path']}" if series.get('backdrop_path') else ''
        })
        list_item.setInfo('video', {
            'plot': series.get('overview', ''),
            'year': series.get('first_air_date', '')[:4]
        })

        url = f"{sys.argv[0]}?action=resolve_torrent&magnet={series['id']}"
        xbmcplugin.addDirectoryItem(
            handle=self.handle,
            url=url,
            listitem=list_item,
            isFolder=False
        )
