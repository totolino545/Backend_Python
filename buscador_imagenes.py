from duckduckgo_search import DDGS

class Buscador_Imagenes:

    @staticmethod
    def buscar_imagenes(nombresArtistas, max_resultados=5):
        try:
            with DDGS() as ddgs:
                resultados = []
                # Buscar imágenes usando DuckDuckGo
                for resultado in ddgs.images(
                    keywords=nombresArtistas,
                    region="wt-wt",
                    safesearch="off",
                    max_results=max_resultados
                ):
                    resultados.append(resultado["image"])
                return resultados
        except Exception as e:
            print(f"Error en la búsqueda: {e}")
            return []
