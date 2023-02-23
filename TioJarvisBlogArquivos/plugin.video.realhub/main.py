import xbmcaddon
import xbmcgui
import xbmcplugin
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


# Define o URL do site a ser raspado
url = "https://vizer.tv/"

# Cria uma função para raspar o site e obter os dados necessários
def scrape_site():
    # Realiza a requisição HTTP para o site
    response = requests.get(url)
    # Parseia o HTML da página utilizando a biblioteca BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Encontra os elementos relevantes para a criação do menu
    menu_items = soup.find_all("div", class_="menu-item")
    # Cria uma lista de dicionários contendo as informações relevantes de cada item do menu
    menu_data = []
    for item in menu_items:
        title = item.find("h3").text
        year = item.find("span", class_="year").text
        description = item.find("p").text
        thumbnail = item.find("img")["src"]
        video_url = item.find("a")["href"]
        # Adiciona as informações em um dicionário
        menu_item = {
            "title": title,
            "year": year,
            "description": description,
            "thumbnail": thumbnail,
            "video_url": video_url
        }
        # Adiciona o dicionário à lista de dados do menu
        menu_data.append(menu_item)
    # Retorna a lista de dados do menu
    return menu_data

# Define uma função para criar o menu no Kodi
def create_menu():
    # Obtém os dados do menu
    menu_data = scrape_site()
    # Define o ID do addon
    addon_id = "plugin.video.realhub"
    # Define o caminho do ícone do addon
    icon = xbmcaddon.Addon(addon_id).getAddonInfo("icon")
    # Cria um objeto de plugin XBMC
    xbmcplugin.setContent(int(sys.argv[1]), "movies")
    # Cria o menu
    for item in menu_data:
        list_item = xbmcgui.ListItem(label=item["title"], label2=item["year"], iconImage=item["thumbnail"], thumbnailImage=item["thumbnail"])
        list_item.setInfo("video", {"title": item["title"], "plot": item["description"], "year": item["year"]})
        list_item.setProperty("IsPlayable", "true")
        list_item.addContextMenuItems([("Reproduzir", "PlayMedia(" + item["video_url"] + ")")])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), item["video_url"], list_item, False)
    # Finaliza a criação do menu
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Define a função para reproduzir o vídeo
def play_video(video_url):
    # Define uma lista de servidores de streaming disponíveis
    servers = ["Server 1", "Server 2", "Server 3"]
    # Cria um objeto de plugin XBMC
    xbmcplugin.setContent(int(sys.argv[1]), "movies")
    # Cria o menu de opções de servidores de streaming
    for server in servers:
        list_item = xbmcgui.ListItem(label=server)
        list_item.setProperty("IsPlayable", "true")
        list_item.addContextMenuItems([("Reproduzir", "PlayMedia(" + video_url + "," + server + ")")])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), video_url, list_item, False)
    # Finaliza a criação do menu
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Define a função principal do addon
def run():
    # Obtém o parâmetro de ação
    params = dict(parse_qs(urlparse(sys.argv[2]).query))
    # Verifica se a ação é para criar o menu
    if not params:
        create_menu()
    # Verifica se a ação é para reproduzir o vídeo
    elif "action" in params and params["action"] == "play":
        video_url = params["url"]
        play_video(video_url)

# Chama a função principal do addon
run()
