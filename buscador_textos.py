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
            # Buscar el div que contiene la letra
        contenedor_letra = sopa.find("div", {"data-lyrics-container": "true"})

        if contenedor_letra:
            # Reemplazar los <br> por saltos de línea y extraer el texto limpio
            letra = contenedor_letra.get_text(separator="\n", strip=True)
            return letra
        else:
            return "Letra no encontrada en la página."
    except Exception as e:
        print(f"Error al extraer la letra: {e}")
        return "Error al obtener la letra."

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

