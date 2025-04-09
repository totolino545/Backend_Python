from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import re

class Buscador_Letras:

    @staticmethod
    def letra_lyricfreak(url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            letra_div = soup.find("div", class_="lyrictxt js-lyrics js-share-text-content")

            if letra_div:
                return letra_div.get_text(separator="\n", strip=True)

            return None
        except Exception as e:
            print(f"Error LyricsFreak: {e}")
            return None

    @staticmethod
    def letra_lyricgenius(url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            bloques = soup.find_all("div", attrs={"data-lyrics-container": "true"})

            if bloques:
                return "\n".join([b.get_text(separator="\n", strip=True) for b in bloques])
            
            return None
        except Exception as e:
            print(f"Error Genius: {e}")
            return None

    @staticmethod
    def buscar_letra(query, max_resultados=5):

        try:
            with DDGS() as ddgs:
                for resultado in ddgs.text(keywords=query, max_results=10):
                    url = resultado["href"]
                    print(f"Probando URL: {url}")

                    if "genius.com" in url:
                        letra = Buscador_Letras.letra_lyricgenius(url)
                    elif "lyricsfreak.com" in url:
                        letra = Buscador_Letras.letra_lyricfreak(url)
                    else:
                        continue

                    if letra:
                        return {
                            "titulo": resultado["title"],
                            "url": url,
                            "letra": letra
                        }
        except Exception as e:
            print(f"Error buscando letra: {e}")
            return {
                "titulo": f"{artista} - {cancion}",
                "url": None,
                "letra": "Letra no encontrada."
            }



