import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
from urllib.parse import urlencode, parse_qsl
from resources.lib.tmdb import TMDbAPI
from resources.lib.debrid import RealDebrid
from resources.lib.utils import logger, get_icon

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    action = params.get('action', 'main_menu')

    tmdb = TMDbAPI(HANDLE)  # Passa HANDLE para a classe

    if action == 'main_menu':
        main_menu()
    elif action == 'list_movies':
        tmdb.list_popular_movies()
    elif action == 'list_series':
        tmdb.list_popular_series()
    elif action == 'search':
        search_content(tmdb)
    elif action == 'resolve_torrent':
        resolve_torrent(params['magnet'])
    elif action == 'play_video':
        play_video(params['url'])
    else:
        xbmcgui.Dialog().notification(ADDON_ID, 'Ação inválida!', xbmcgui.NOTIFICATION_ERROR)

def main_menu():
    add_directory_item(
        label='Filmes Populares',
        action='list_movies',
        icon=get_icon('movies.png')
    )
    add_directory_item(
        label='Séries em Alta',
        action='list_series',
        icon=get_icon('series.png')
    )
    add_directory_item(
        label='Pesquisar',
        action='search',
        icon=get_icon('search.png')
    )
    xbmcplugin.endOfDirectory(HANDLE)

def add_directory_item(label, action, icon, is_folder=True, **kwargs):
    url = f'{BASE_URL}?{urlencode({"action": action, **kwargs})}'
    list_item = xbmcgui.ListItem(label=label)
    list_item.setArt({'icon': icon, 'thumb': icon})
    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=list_item,
        isFolder=is_folder
    )

def search_content():
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Pesquisar Filme/Série')
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if query:
            TMDbAPI().search_content(query)

def resolve_torrent(magnet):
    rd_token = ADDON.getSettingString('realdebrid_token')
    if not rd_token:
        xbmcgui.Dialog().ok(ADDON_NAME, 'Configure o Real-Debrid nas configurações!')
        return

    debrid = RealDebrid(rd_token)
    stream_url = debrid.resolve_magnet(magnet)
    if stream_url:
        play_video(stream_url)
    else:
        xbmcgui.Dialog().notification(ADDON_NAME, 'Link inválido!', xbmcgui.NOTIFICATION_ERROR)

def play_video(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(HANDLE, True, play_item)

if __name__ == '__main__':
    logger(f'Iniciando {ADDON_NAME}...')
    router(sys.argv[2][1:])
