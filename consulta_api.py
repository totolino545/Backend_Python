import requests

def obtener_radios(genero='blues'):
    url = f'https://zeno.fm/api/stations/?query={genero}&limit=200&genre=Music'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), 200
    except requests.RequestException as e:
        return {'error': str(e)}, 500

def obtener_radio_por_id(radio_id):
    url = f'https://zeno.fm/api/stations/{radio_id}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), 200
    except requests.RequestException as e:
        return {'error': str(e)}, 500

