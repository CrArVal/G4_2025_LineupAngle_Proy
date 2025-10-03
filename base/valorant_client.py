# base/valorant_client.py
import requests

BASE_URL = "https://valorant-api.com/v1"  # dominio principal de la API pública

def get_agents(is_playable=True, language="es-ES"):
    url = f"{BASE_URL}/agents"
    params = {
        "isPlayableCharacter": str(is_playable).lower(),
        "language": language
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
  # devuelve diccionario
def get_weapons(language="es-ES"):
    url = f"{BASE_URL}/weapons"
    params = {"language": language}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def get_maps(language="es-ES"):
    url = f"{BASE_URL}/maps"
    params = {"language": language}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()