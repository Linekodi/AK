import xbmc
import xbmcgui
import xbmcplugin
import requests
import xbmcaddon

# Pega a chave da API do Real-Debrid nas configurações do Kodi
addon = xbmcaddon.Addon()

def get_elementum_links(query):
    """
    Função para buscar links do Elementum.

    :param query: O nome ou termo de busca.
    :return: Links encontrados ou None em caso de erro.
    """
    base_url = "http://127.0.0.1:6800/jsonrpc"
    headers = {
        "Content-Type": "application/json"
    }

    # Monta o payload da requisição
    payload = {
        "jsonrpc": "2.0",
        "method": "aria2.search",
        "params": [query],
        "id": 1
    }

    try:
        # Faz a requisição HTTP para o Elementum
        response = requests.post(base_url, json=payload, headers=headers)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP

        # Extrai e retorna os links encontrados
        data = response.json()
        if "result" in data:
            return data["result"]
        else:
            xbmc.log(f"Nenhum link encontrado para: {query}", level=xbmc.LOGINFO)
            return None
    except requests.exceptions.RequestException as e:
        xbmc.log(f"Erro ao acessar Elementum: {e}", level=xbmc.LOGERROR)
        return None
