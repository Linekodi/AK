import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import xbmc
from resources.lib.scraper import *

if len(sys.argv) > 1:
    addon_handle = int(sys.argv[1])
else:
    addon_handle = -1

# Define as URLs de cada tipo de mídia
MOVIES_URL = 'https://warezcdn.com/listing.php?type=movies'
SERIES_URL = 'https://warezcdn.com/listing.php?type=series'
ANIMES_URL = 'https://warezcdn.com/listing.php?type=animes'

# Define o handle do addon e a URL base
addon_handle = int(sys.argv[1])
addon_url = sys.argv[0]

# Cria uma função para exibir a lista de mídia
def list_media(media_type):
    url = None
    if media_type == 'movie':
        url = MOVIES_URL
    elif media_type == 'series':
        url = SERIES_URL
    elif media_type == 'anime':
        url = ANIMES_URL
    if url is not None:
        html = get_url(url)
        media = extract_media_info(html)
        for item in media:
            list_item = xbmcgui.ListItem(label=item['title'])
            list_item.setArt({'thumb': item['image'], 'icon': 'DefaultVideo.png'})
            url = addon_url({'mode': 'play', 'type': media_type, 'title': item['title'], 'link': item['link']})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=False)
        xbmcplugin.endOfDirectory(addon_handle)

# Cria uma função para reproduzir um item de mídia
def play_media(title, link):
    url = get_media_url(link)
    list_item = xbmcgui.ListItem(label=title)
    list_item.setArt({'icon': 'DefaultVideo.png'})
    list_item.setPath(url)
    xbmcplugin.setResolvedUrl(addon_handle, True, list_item)

# Cria uma função para pesquisar conteúdo
def search_media():
    keyboard = xbmc.Keyboard('', 'Pesquisar conteúdo')
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        html = search_url(query)
        media = extract_media_info(html)
        for item in media:
            list_item = xbmcgui.ListItem(label=item['title'])
            list_item.setArt({'thumb': item['image'], 'icon': 'DefaultVideo.png'})
            url = addon_url({'mode': 'play', 'type': item['type'], 'title': item['title'], 'link': item['link']})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=list_item, isFolder=False)
        xbmcplugin.endOfDirectory(addon_handle)

# Verifica o modo de execução do addon e chama a função correspondente
params = dict(parse_qsl(sys.argv[2][1:]))
mode = params.get('mode', None)
if mode is None:
    # Exibe o menu principal
    list_item = xbmcgui.ListItem(label='RealHub')
    xbmcplugin.setPluginCategory(addon_handle, 'RealHub')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=addon_url({'mode': 'list_movies'}), listitem=list_item, isFolder=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=addon_url({'mode': 'list_series'}), listitem=list_item, isFolder=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=addon_url({'mode': 'list_animes'}), listitem=list_item, isFolder=True)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=addon_url({'mode': 'search'}), listitem=list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode == 'list_movies':
    # Exibe a lista de filmes
    list_media('movie')
elif mode == 'list_series':
    # Exibe a lista de séries
    list_media('series')
elif mode == 'list_animes':
    # Exibe a lista de animes
    list_media('anime')
elif mode == 'search':
    # Permite pesquisar conteúdo
    search_media()
elif mode == 'play':
    # Reproduz um item de mídia
    play_media(params['title'], params['link'])
