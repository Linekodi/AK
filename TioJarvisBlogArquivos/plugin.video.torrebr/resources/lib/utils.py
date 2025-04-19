import os
import xbmc
import xbmcaddon
import random

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')

def logger(message, level=xbmc.LOGINFO):
    xbmc.log(f"[TorreBR] {str(message)}", level)

def get_icon(name):
    icons_dir = os.path.join(ADDON_PATH, 'resources', 'media')
    default_icon = os.path.join(icons_dir, 'default_icon.png')
    icon_path = os.path.join(icons_dir, name)
    return icon_path if os.path.exists(icon_path) else default_icon

def build_url(query):
    return f"{sys.argv[0]}?{urlencode(query)}"

def get_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15',  # String corrigida
        'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
    ]
    return {'User-Agent': random.choice(agents)}

def size_to_gb(size_bytes):
    try:
        return f"{int(size_bytes)/(1024**3):.1f} GB"
    except:
        return "N/A"
