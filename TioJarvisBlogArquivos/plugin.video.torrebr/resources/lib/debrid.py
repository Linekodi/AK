import xbmcgui
import requests
from urllib.parse import quote
from resources.lib.utils import logger

class RealDebrid:
    BASE_URL = "https://api.real-debrid.com/rest/1.0"
    OAUTH_URL = "https://api.real-debrid.com/oauth/v2"

    def __init__(self, api_token):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.api_token}'})

    def resolve_magnet(self, magnet_url):
        """Transforma um magnet link em URL de streaming"""
        if not self.api_token:
            logger("Token do Real-Debrid não configurado!", xbmc.LOGERROR)
            return None

        try:
            # Etapa 1: Adicionar magnet
            torrent_id = self._add_magnet(magnet_url)
            if not torrent_id:
                return None

            # Etapa 2: Selecionar arquivo principal (maior tamanho)
            file_id = self._select_file(torrent_id)
            if not file_id:
                return None

            # Etapa 3: Obter link direto
            return self._get_download_link(torrent_id, file_id)

        except Exception as e:
            logger(f"Erro ao resolver torrent: {str(e)}", xbmc.LOGERROR)
            return None

    def _add_magnet(self, magnet):
        response = self.session.post(
            f"{self.BASE_URL}/torrents/addMagnet",
            data={'magnet': magnet}
        )
        return response.json().get('id') if response.status_code == 201 else None

    def _select_file(self, torrent_id):
        response = self.session.get(f"{self.BASE_URL}/torrents/info/{torrent_id}")
        if response.status_code != 200:
            return None

        files = response.json().get('files', [])
        # Seleciona o arquivo com maior tamanho (normalmente o vídeo principal)
        main_file = max(files, key=lambda x: x['bytes'], default=None)
        return main_file.get('id') if main_file else None

    def _get_download_link(self, torrent_id, file_id):
        response = self.session.post(
            f"{self.BASE_URL}/torrents/selectFiles/{torrent_id}",
            data={'files': str(file_id)}
        )
        if response.status_code == 204:
            info = self.session.get(f"{self.BASE_URL}/torrents/info/{torrent_id}").json()
            return info.get('links', [None])[0]
        return None

    @staticmethod
    def auth_device():
        """Gera URL de autenticação (para implementação futura)"""
        response = requests.post(f"{RealDebrid.OAUTH_URL}/device/code", data={
            'client_id': 'X245A4XAIBGVM',
            'new_credentials': 'yes'
        })
        return response.json()
