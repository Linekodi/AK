import requests
import xbmc
import xbmcgui
from bs4 import BeautifulSoup

def scrape_website_for_links(url):
    """
    Função para fazer scraping em um site para pegar links de conteúdo.

    :param url: URL do site para scraping.
    :return: Lista de links encontrados no site.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Levanta exceção em caso de erro na requisição

        # Usa o BeautifulSoup para fazer parsing do conteúdo HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Procura links no HTML
        links = []
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if 'http' in link:  # Filtra links válidos
                links.append(link)

        return links

    except requests.exceptions.RequestException as e:
        xbmc.log(f"Erro ao fazer scraping no site {url}: {e}", level=xbmc.LOGERROR)
        return []
