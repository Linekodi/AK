# -*- coding: utf-8 -*-

# Importa as bibliotecas necessárias
from xbmcaddon import Addon

# Define o addon
addon = Addon()
addon_id = addon.getAddonInfo('id')

# Define as configurações padrão
DEFAULTS = {
    'file_url': '',
    'enable_adult_content': False,
    'cache_size': 50,
    'default_language': 'en_us',
}

class Settings:
    def __init__(self):
        self.settings = addon.getAddonInfo('settings')
        self.read_settings()

    def read_settings(self):
        self.file_url = addon.getSetting(self.settings.get('file_url'))
        self.enable_adult_content = addon.getSetting(self.settings.get('enable_adult_content')) == 'true'  # Convert string to bool
        self.cache_size = int(addon.getSetting(self.settings.get('cache_size')))
        self.default_language = addon.getSetting(self.settings.get('default_language'))

    def save_settings(self):
        addon.setSetting(self.settings.get('file_url'), self.file_url)
        addon.setSetting(self.settings.get('enable_adult_content'), str(self.enable_adult_content))  # Convert bool to string
        addon.setSetting(self.settings.get('cache_size'), str(self.cache_size))
        addon.setSetting(self.settings.get('default_language'), self.default_language)

# Código fim
