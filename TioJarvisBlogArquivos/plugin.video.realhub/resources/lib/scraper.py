import requests
from bs4 import BeautifulSoup

# URL base do site que estamos raspando
BASE_URL = 'https://warezcdn.com'

# Cria uma função para fazer uma requisição HTTP e retornar o HTML da página
def get_url(url):
    response = requests.get(url)
    return response.text

# Cria uma função para extrair informações de mídia de uma página HTML
def extract_media_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    media = []
    for item in soup.select('div.card'):
        title = item.select_one('h5.card-title a').text.strip()
        link = item.select_one('h5.card-title a')['href']
        image = item.select_one('img.card-img')['src']
        type = get_media_type(link)
        media.append({'title': title, 'link': link, 'image': image, 'type': type})
    return media

# Cria uma função para obter o tipo de mídia com base na URL do link
def get_media_type(link):
    if '/listing.php?type=movies' in link:
        return 'movie'
    elif '/listing.php?type=series' in link:
        return 'series'
    elif '/listing.php?type=animes' in link:
        return 'anime'
    else:
        return 'unknown'

# Cria uma função para obter a URL de reprodução da mídia
def get_media_url(link):
    html = get_url(BASE_URL + link)
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.select_one('div#player iframe')['src']
    return url
