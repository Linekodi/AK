import xbmcgui
import xbmcplugin
import re
import requests
import sys

BASE_URL = 'https://pastebin.com/raw/MUaRqjYd'

def get_params():
    paramstring = sys.argv[2]
    params = dict(re.findall("([^&]+)=([^&]+)", paramstring))
    return params

def warezPlugin(type, imdb, season, episode):
    if (type == "filme"):
        season = ""
        episode = ""
    else:
        if (season != ""):
            season = "/" + season
        if (episode != ""):
            episode = "/" + episode

    frame = '<iframe src="https://embed.warezcdn.com/{}/{}/{}{}" scrolling="no" frameborder="0" allowfullscreen="" webkitallowfullscreen="" mozallowfullscreen=""></iframe>'.format(type, imdb, season, episode)

    return frame

def listar_filmes():
    url = BASE_URL + '/movies'

    response = requests.get(url)

    filmes = response.json()

    for filme in filmes:
        imdb = filme['imdb']
        nome = filme['nome']

        url = build_url({
            'mode': 'assistir_filme',
            'imdb': imdb,
        })

        list_item = xbmcgui.ListItem(label=nome)
        list_item.setInfo('video', {'title': nome})
        list_item.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=False)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def listar_series():
    url = BASE_URL + '/series'

    response = requests.get(url)

    series = response.json()

    for serie in series:
        imdb = serie['imdb']
        nome = serie['nome']

        url = build_url({
            'mode': 'assistir_serie',
            'imdb': imdb,
        })

        list_item = xbmcgui.ListItem(label=nome)
        list_item.setInfo('video', {'title': nome})
        list_item.setProperty('IsPlayable', 'true')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=list_item, isFolder=True)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def assistir_filme(imdb):
    url = warezPlugin('filme', imdb, '', '')
    list_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, list_item)

def assistir_serie(imdb):
    url = warezPlugin('serie', imdb, '1', '1')
    list_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, list_item)

def build_url(query):
    return sys.argv[0] + '?' + urlencode(query)

params = get_params()
mode = params['mode']

if mode == 'listar_filmes':
    listar_filmes()
elif mode == 'listar_series':
    listar_series()
elif mode == 'assistir_filme':
    imdb = params['imdb']
    assistir_filme(imdb)
elif mode == 'assistir_serie':
    imdb = params['imdb']
    assistir_serie(imdb)
