# -*- coding: utf-8 -*-

# Importa as bibliotecas necessárias
import xbmcaddon
import xbmcgui
import os
from .core import Core
from .gui import GUI
from .settings import Settings
# Importa o módulo utilitário
from .utils import Utils

# Define o addon
addon_id = 'plugin.video.tiojarvis-addonbase'
addon = xbmcaddon.Addon(addon_id)

# Define o path do addon
addon_path = os.path.join(addon.getAddonInfo('path'), '')

# Define o logger do addon
logger = addon.getAddonInfo('name')

# Carrega os módulos principais
from .core import Core
from .gui import GUI
from .settings import Settings
from .utils import Utils

# Cria instâncias dos módulos
core = Core()
gui = GUI()
settings = Settings()
utils = Utils()

# Código fim


