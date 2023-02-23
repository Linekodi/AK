# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcplugin
import re
import requests

class Player:
    def __init__(self):
        pass

    def play(self, url):
        try:
            source_code = requests.get(url).text
            media_urls = re.findall('"file":"(.*?)"', source_code)
            listitem = xbmcgui.ListItem(path=media_urls[0])
            xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
        except:
            xbmc.log('Could not play video: ' + url, xbmc.LOGERROR)

