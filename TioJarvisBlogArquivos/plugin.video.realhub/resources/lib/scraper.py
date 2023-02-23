import requests
import re

# URLs das páginas de mídia
MOVIES_URL = 'https://warezcdn.com/listing.php?type=movies'
SERIES_URL = 'https://warezcdn.com/listing.php?type=series'
ANIMES_URL = 'https://warezcdn.com/listing.php?type=animes'

# Expressões regulares para extrair informações do HTML
TITLE_REGEX = r'<div class="mvic-desc">\s*<a href=".+?">\s*(.+?)\s*</a>\s*</div>'
IMAGE_REGEX = r'<div class="mvic-thumb">\s*<a href=".+?">\s*<img src="(.+?)"'
URL_REGEX = r'<div class="mvic-desc">\s*<a href="(.+?)">\s*.+?\s*</a>\s*</div>'


def get_url(url):
    """
    Realiza uma solicitação GET para uma URL e retorna o conteúdo da resposta.
    """
    response = requests.get(url)
    return response.content.decode('utf-8')


def extract_media_info(html):
    """
    Extrai informações de mídia (título, imagem e URL) do HTML da página.
    """
    titles = re.findall(TITLE_REGEX, html)
    images = re.findall(IMAGE_REGEX, html)
    urls = re.findall(URL_REGEX, html)

    media = []
    for i in range(len(titles)):
        media.append({
            'title': titles[i],
            'image': images[i],
            'url': urls[i]
        })
    return media
