import os
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")


def buscar_jogos(nome):
    if not RAWG_API_KEY:
        return []

    url = "https://api.rawg.io/api/games"

    params = {
        "key": RAWG_API_KEY,
        "search": nome,
        "page_size": 6,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        dados = response.json()

        return dados.get("results", [])

    except requests.RequestException:
        return []
    
def buscar_detalhes_jogo(rawg_id):

    url = f"https://api.rawg.io/api/games/{rawg_id}"

    params = {
        "key": RAWG_API_KEY,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        dados = response.json()

        descricao_original = dados.get(
            'description_raw',
            ''
        )

        try:

            descricao_traduzida = GoogleTranslator(
                source='auto',
                target='pt'
            ).translate(descricao_original)

        except:

            descricao_traduzida = descricao_original

        dados['descricao_traduzida'] = descricao_traduzida

        return dados

    except requests.RequestException:

        return None