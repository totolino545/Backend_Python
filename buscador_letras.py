from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

class Buscador_Letras:
    
    @staticmethod
    def extraer_letra(url):
        """Extrae texto de una página web, incluyendo letras de canciones si están en un contenedor específico."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            respuesta = requests.get(url, headers=headers, timeout=5)
            respuesta.raise_for_status()

            sopa = BeautifulSoup(respuesta.text, "html.parser")

            # Buscar contenedor con letras de canciones
            contenedor_letra = sopa.find("div", {"data-lyrics-container": "true"})
            if contenedor_letra:
                return contenedor_letra.get_text(separator="\n", strip=True)
            
            # Si no hay letras, buscar párrafos normales como texto alternativo
            parrafos = sopa.find_all("p")
            texto = " ".join([p.get_text() for p in parrafos])

            return texto[:2000] if texto else "No se encontró contenido útil."
        except Exception as e:
            print(f"Error extrayendo texto de {url}: {e}")
            return "Error al obtener el contenido."

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


