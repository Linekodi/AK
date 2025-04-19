import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from urllib.parse import urlencode, parse_qsl, quote
from resources.lib.tmdb import TMDbAPI
from resources.lib.debrid import RealDebrid
from resources.lib.providers import TorrentProviders
from resources.lib.utils import logger, get_icon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    action = params.get('action', 'main_menu')

    if action == 'main_menu':
        main_menu()
    elif action == 'list_movies':
        TMDbAPI(HANDLE).list_popular_movies()
    elif action == 'list_series':
        TMDbAPI(HANDLE).list_popular_series()
    elif action == 'search':
        search_content()
    elif action == 'search_torrents':
        title = params.get('title')
        list_torrents(title)
    elif action == 'resolve_torrent':
        resolve_torrent(params['magnet'])
    elif action == 'play_video':
        play_video(params['url'])
    else:
        xbmcgui.Dialog().notification(ADDON_ID, 'Ação inválida!', xbmcgui.NOTIFICATION_ERROR)
    xbmcplugin.endOfDirectory(HANDLE)

def main_menu():
    add_directory_item('Filmes Populares', 'list_movies', get_icon('movies.png'))
    add_directory_item('Séries em Alta', 'list_series', get_icon('series.png'))
    add_directory_item('Pesquisar', 'search', get_icon('search.png'))

def add_directory_item(label, action, icon, is_folder=True, **kwargs):
    url = f'{BASE_URL}?{urlencode({"action": action, **kwargs})}'
    li = xbmcgui.ListItem(label=label)
    li.setArt({'icon': icon, 'thumb': icon})
    xbmcplugin.addDirectoryItem(HANDLE, url, li, is_folder)

def search_content():
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Pesquisar Filme/Série')
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if query:
            TMDbAPI(HANDLE).search_content(query)

def list_torrents(title):
    providers = TorrentProviders()
    torrents = providers.search_torrents(title)
    if torrents:
        for torrent in torrents:
            add_directory_item(
                label=f"{torrent['name']} [Seeders: {torrent.get('seeders', 0)}]",
                action='resolve_torrent',
                icon=get_icon('torrent.png'),
                magnet=torrent['magnet']
            )
    else:
        xbmcgui.Dialog().notification(ADDON_ID, 'Nenhum torrent encontrado!', xbmcgui.NOTIFICATION_WARNING)

def resolve_torrent(magnet):
    rd_token = ADDON.getSettingString('realdebrid_token')
    if not rd_token:
        xbmcgui.Dialog().ok(ADDON_ID, 'Configure o Real-Debrid nas configurações!')
        return

    debrid = RealDebrid(rd_token)
    stream_url = debrid.resolve_magnet(magnet)
    if stream_url:
        play_video(stream_url)
    else:
        xbmcgui.Dialog().notification(ADDON_ID, 'Link inválido!', xbmcgui.NOTIFICATION_ERROR)

def play_video(url):
    li = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

if __name__ == '__main__':
    logger(f'Iniciando {ADDON_ID}...')
    router(sys.argv[2][1:])
