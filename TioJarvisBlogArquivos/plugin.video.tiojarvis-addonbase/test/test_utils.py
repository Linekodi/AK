# -*- coding: utf-8 -*-

# Importa as bibliotecas necessárias
from xbmcaddon import Addon
from xbmcgui import Dialog

# Define o addon
addon = Addon()
addon_id = addon.getAddonInfo('id')

# Função para exibir um diálogo de notificação
def show_notification(message, title="TioJarvis - Addon Base"):
    dialog = Dialog(addon_id)
    dialog.ok(title, message)

# Função para exibir um diálogo de confirmação
def confirm_action(message, title="TioJarvis - Addon Base"):
    dialog = Dialog(addon_id)
    return dialog.yesno(title, message)

# Função para exibir um diálogo de entrada de texto
def get_user_input(message, title="TioJarvis - Addon Base"):
    dialog = Dialog(addon_id)
    return dialog.input(title, message)

# Código fim
