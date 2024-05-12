# -*- coding: utf-8 -*-

# Importa as bibliotecas necessárias
from xbmcaddon import Addon
from xbmcgui import Window, ListItem, Dialog
from .core import Core

# Define o addon
addon = Addon()
addon_id = addon.getAddonInfo('id')

# Classe principal da GUI
class GUI:
    def __init__(self):
        self.window = Window(1080)
        self.font = self.window.getSkinFont()
        self.core = Core()

    def show_main_menu(self):
        # Criar o menu principal e definir as ações dos itens
        menu = []
        menu.append(ListItem(label="Filmes", action="RunPlugin(plugin.video.tiojarvis-addonbase?action=show_movies)"))
        menu.append(ListItem(label="Séries", action="RunPlugin(plugin.video.tiojarvis-addonbase?action=show_series)"))
        menu.append(ListItem(label="Configurações", action="RunPlugin(plugin.video.tiojarvis-addonbase?action=show_settings)"))
        self.window.clearList()
        self.window.addItems(menu)
        self.window.setListItemFont(self.font)
        self.window.setTitle("TioJarvis - Addon Base")
        self.window.doModal()

    def show_movies_list(self):
        # Listar os filmes recuperados do core
        movies = self.core.movies_data
        if not movies:
            self.show_notification("Nenhum filme encontrado.")
            return

        menu = []
        for movie in movies:
            list_item = ListItem(label=movie['title'])
            list_item.setArt({'thumb': "", 'fanart': "", 'poster': ""})  # (Definir artwork se disponível)
            list_item.setInfo(type="video", infoLabels={"title": movie['title']})  # (Definir informações adicionais)
            list_item.setProperty("IsPlayable", "true")
            list_item.setAction("RunPlugin(plugin.video.tiojarvis-addonbase?action=play_movie&url=" + movie['url'] + ")")
            menu.append(list_item)

        self.window.clearList()
        self.window.addItems(menu)
        self.window.setListItemFont(self.font)
        self.window.setTitle("Filmes")
        self.window.doModal()

    def show_series_list(self):
        # Implementar a lógica para mostrar a lista de séries (utilizar o core.series_data)
        # ... (similar ao show_movies_list)
        # ...
        self.show_notification("Funcionalidade de séries ainda não implementada.")

    def show_movie_details(self, movie_id):
        # Exibir detalhes do filme selecionado (utilizar o core.get_movie_details)
        # ... (implementar a lógica para exibir detalhes)
        # ...
        self.show_notification("Funcionalidade de detalhes de filme ainda não implementada.")

    def show_settings(self):
        # Abrir a janela de configurações do addon
        addon.openSettings()

    def show_notification(self, message, title="TioJarvis - Addon Base"):
        dialog = Dialog(addon_id)
        dialog.ok(title, message)

    def play_movie(self, url):
        # Reproduzir o filme selecionado (utilizar o xbmc.Player)
        player = xbmc.Player()
        player.play(url)

# Código fim
