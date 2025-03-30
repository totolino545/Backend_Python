from duckduckgo_search import DDGS

class Buscador_Textos:

    @staticmethod
    def buscar_textos(query, max_resultados):
        try:
            with DDGS() as ddgs:
                resultados = []
                # Buscar textos usando DuckDuckGo
                for resultado in ddgs.text(
                    keywords=query,
                    region="wt-wt",
                    safesearch="moderate",
                    max_results=max_resultados
                ):
                    # Almacenar título, URL y fragmento del resultado
                    resultados.append({
                        "titulo": resultado["title"],
                        "url": resultado["href"],
                        "snippet": resultado["body"]
                    })                  
                return resultados
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []
