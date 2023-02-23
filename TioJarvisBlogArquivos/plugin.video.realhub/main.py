import sys
import xbmcaddon
from urllib.parse import urlparse, parse_qs
from resources.lib import scraper

addon_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')

def run():
    params = dict(parse_qs(urlparse(sys.argv[2]).query))
    mode = params.get('mode', None)
    if mode is None:
        scraper.create_menu()
    elif mode == 'play':
        video_url = params['url'][0]
        scraper.play_video(video_url)

if __name__ == '__main__':
    run()
