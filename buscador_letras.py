from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup, Comment

class Buscador_Letras:
    
    @staticmethod
    def extraer_letra(url):
        """Extrae texto de una página web, incluyendo letras de canciones si están en un contenedor específico."""
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            letra_div = soup.find("div", class_="lyrictxt js-lyrics js-share-text-content")

            if letra_div:
                letra = letra_div.get_text(separator="\n", strip=True)
                return letra
            else:
                return "Letra no encontrada."
        except Exception as e:
            print(f"Error al obtener la letra desde LyricsFreak: {e}")
            return "Error al obtener la letra."

    @staticmethod
    def buscar_letra(artista, cancion, max_resultados=3):
        """Busca una canción en LyricsFreak usando DuckDuckGo y devuelve la letra."""
        query = f"{artista} {cancion} site:lyricsfreak.com"

        try:
            with DDGS() as ddgs:
                for resultado in ddgs.text(keywords=query, max_results=max_resultados):
                    url = resultado["href"]
                    if "lyricsfreak.com" in url:
                        letra = LetrasLyricsFreak.extraer_letra(url)
                        return {
                            "titulo": resultado["title"],
                            "url": url,
                            "letra": letra
                        }
            return {"error": "No se encontró letra."}
        except Exception as e:
            return {"error": f"Error durante la búsqueda: {e}"}


