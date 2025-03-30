from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

class Buscador_Textos:
    
    @staticmethod
    def extraer_texto(url):
        """Obtiene el texto principal de una página web."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            respuesta = requests.get(url, headers=headers, timeout=5)
            respuesta.raise_for_status()
            
            sopa = BeautifulSoup(respuesta.text, "html.parser")
            parrafos = sopa.find_all("data-Lyrics__Container")
            texto = " ".join([p.get_text() for p in parrafos])

            return texto[:2000]  # Límite para evitar respuestas demasiado largas
        except Exception as e:
            print(f"Error extrayendo texto de {url}: {e}")
            return ""

    @staticmethod
    def buscar_textos(query, max_resultados):
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
                    texto_ampliado = Buscador_Textos.extraer_texto(url)

                    resultados.append({
                        "titulo": resultado["title"],
                        "url": url,
                        "snippet": resultado["body"],
                        "texto_completo": texto_ampliado
                    })

                return resultados
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []

