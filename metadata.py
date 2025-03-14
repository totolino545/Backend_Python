import requests

class Metadatos:

    @staticmethod
    def obtener_metadatos_shoutcast(url):
        headers = {
            'Icy-MetaData': '1',
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            response = requests.get(url, headers=headers, stream=True)

            if 'icy-metaint' in response.headers:
                metaint = int(response.headers['icy-metaint'])
                for chunk in response.iter_content(chunk_size=metaint + 255):
                    if len(chunk) < metaint:
                        continue
                    metadata = chunk[metaint:].split(b'\0', 1)[0]
                    metadata_str = metadata.decode('utf-8', errors='replace')

                    if "StreamTitle=" in metadata_str:
                        title = metadata_str.split('StreamTitle=')[1].split(';')[0].strip("'")
                        return title

                print("No se encontraron metadatos ICY en la transmisión.")
            else:
                print("El servidor no proporciona metadatos ICY.")

        except Exception as e:
            print(f"Error al intentar leer metadatos: {e}")

        return None
