# -*- coding: utf-8 -*-
import sys
import xbmcgui
import xbmcplugin
from resources.lib.realhub import Realhub

addon_handle = int(sys.argv[1])
realhub = Realhub()

def list_categories():
    categories = realhub.scraper.get_categories()
    for category in categories:
        url = category['url']
        label = category['title']
        list_item = xbmcgui.ListItem(label=label)
        list_item.setArt({'icon': category['thumbnail']})
        list_item.setInfo('video', {'title': label})
        url_params = {'mode': 'list_videos', 'url': url}
        xbmcplugin.addDirectoryItem(addon_handle, sys.argv[0] + '?' + urlencode(url_params), list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_videos():
    url = sys.argv[2]
    videos = realhub.scraper.get_videos(url)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['title'])
        list_item.setArt({'icon': video['thumbnail']})
        list_item.setInfo('video', {'title': video['title'], 'plot': video['description']})
        url_params = {'mode': 'play_video', 'url': video['url']}
        xbmcplugin.addDirectoryItem(addon_handle, sys.argv[0] + '?' + urlencode(url_params), list_item)
    xbmcplugin.endOfDirectory(addon_handle)

def play_video():
    url = sys.argv[2]
    realhub.player.play(url)

mode = args.get('mode', None)
if mode is None:
    list_categories()
elif mode == 'list_videos':
    list_videos()
elif mode == 'play_video':
    play_video()

