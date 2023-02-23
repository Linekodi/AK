import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://vizer.tv'

def create_menu():
    url = BASE_URL + '/lista'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.select('.movies-list .ml-item')
    for item in items:
        title = item.select_one('.ml-mask strong').text
        thumb = item.select_one('.ml-img img')['src']
        video_url = item.select_one('.ml-mask')['href']
        li = xbmcgui.ListItem(label=title)
        li.setArt({'thumb': thumb})
        li.setInfo(type='video', infoLabels={'title': title})
        url = BASE_URL + video_url
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li)

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play_video(video_url):
    html = requests.get(video_url).content
    soup = BeautifulSoup(html, 'html.parser')
    sources = soup.select('.mirrors-links li')
    for source in sources:
        server_name = source.select_one('.mirror-name').text.strip()
        link = source.select_one('.mirror-link a')['href']
        li = xbmcgui.ListItem(label=server_name)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=link, listitem=li)

    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=sources[0].select_one('.mirror-link a')['href']))
