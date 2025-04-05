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
                        ),
                        "Referer": "https://www.google.com/",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1"
                    }

            respuesta = requests.get(url, headers=headers, timeout=10)
            respuesta.raise_for_status()

            sopa = BeautifulSoup(respuesta.text, "html.parser")
            print(sopa)
            # Buscar el <div> que contenga el comentario específico
            for div in sopa.find_all("div"):
                comentarios = div.find_all(string=lambda text: isinstance(text, Comment))
                for comentario in comentarios:
                    if "Usage of azlyrics.com content" in comentario:
                        texto = div.get_text(separator="\n", strip=True)
                        return texto

            return "No se encontró la letra en AZLyrics."
        except Exception as e:
            print(f"Error extrayendo texto de {url}: {e}")
            return "Error al obtener el contenido"

    @staticmethod
    def buscar_letras(query, max_resultados):
        """Busca resultados en DuckDuckGo y extrae texto de las páginas obtenidas."""
        try:
            with DDGS() as ddgs:
                resultados = []
                for resultado in ddgs.text(
                    keywords=query,
                    region="wt-wt",
                    safesearch="moderate",
                    max_results=max_resultados
                ):
                    url = resultado["href"]
                    resultados.append({
                        "titulo": resultado["title"],
                        "url": url,
                        "snippet": resultado["body"],
                        "texto_completo": Buscador_Letras.extraer_letra(url)
                    })

                return resultados
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []


