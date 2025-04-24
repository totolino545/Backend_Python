import requests, json

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

def obtener_metadata_por_id(id):
    url = f'https://api.zeno.fm/mounts/metadata/subscribe/{id}'
    try:
        with requests.get(url, stream=True, timeout=10) as response:
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data:"):
                    # Extraer la parte JSON del mensaje
                    data_str = line.removeprefix("data:").strip()
                    try:
                        data = json.loads(data_str)
                        stream_title = data.get("streamTitle", "")
                        if " - " in stream_title:
                            artist, song = stream_title.split(" - ", 1)
                        else:
                            artist, song = "Desconocido", stream_title

                        return {
                            "artist": artist.strip(),
                            "song": song.strip()
                        }, 200
                    except Exception as e:
                        return {"error": f"Error parseando JSON: {e}"}, 500

        return {"error": "No se recibieron metadatos"}, 404

    except requests.RequestException as e:
        return {"error": str(e)}, 500

