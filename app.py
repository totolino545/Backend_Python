from flask import Flask, request, jsonify, json
import os
from flask_cors import CORS
from traductor import Traducir
from metadata import Metadatos
from buscador_imagenes import Buscador_Imagenes
from buscador_textos import buscar_textos
from duckduckgo_search import DDGS


app = Flask(__name__)
CORS(app)  # Esto habilita CORS para toda la app
traductor = Traducir()  # Instancia correcta del traductor
metadata = Metadatos()  # Instancia correcta de los metadatos
buscador = Buscador_Imagenes()  # Instancia correcta del buscador de imágenes
buscador_textos = buscar_textos()  # Instancia correcta del buscador de textos

@app.route('/')
def home():
    return "¡Hola desde Railway!"

@app.route('/traducir', methods=['GET'])
def obtener_traduccion():
    texto = request.args.get('texto')
    
    if not texto:
        return jsonify({'error': 'Parámetro "texto" requerido'}), 400
    
    # Llamar al método de la INSTANCIA
    resultado, codigo_estado = traductor.traducir_texto(texto)
    return jsonify(resultado), codigo_estado

@app.route('/metadata', methods=['GET'])
def cargar_metadata():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'Parámetro "url" requerido'}), 400

    try:
        metadato = metadata.obtener_metadatos_shoutcast(url)
        if not metadato:
            return jsonify({'error': 'No se encontraron metadatos'}), 404
        return jsonify({'metadata': metadato})
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/imagenes', methods=['GET'])
def cargar_imagenes():
    json_artistas = request.args.get('json_artistas')
    if not json_artistas:
        return jsonify({'error': 'Parámetro "json_artistas" requerido'}), 400
    
    try:
        # Parsear el JSON a una lista de artistas
        lista_artistas = json.loads(json_artistas)
        
        # Validar que sea una lista y tenga máximo 5 elementos
        if not isinstance(lista_artistas, list) or len(lista_artistas) > 5:
            return jsonify({'error': 'El parámetro debe ser un JSON array con máximo 5 artistas'}), 400
        
        resultados = {}
        for artista in lista_artistas:
            # Buscar imágenes para cada artista
            imagenes = buscador.buscar_imagenes(artista)
            resultados[artista] = imagenes if imagenes else []
        
        return jsonify(resultados)
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Formato JSON inválido'}), 400
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/texto', methods=['GET'])
def obtener_traduccion():
    texto = request.args.get('texto')
    
    if not texto:
        return jsonify({'error': 'Parámetro "texto" requerido'}), 400

    resultados = buscar_textos(texto, max_resultados=5)
    
    if resultados:
        print(f"Resultados de búsqueda para '{query}':\n")
        for i, res in enumerate(resultados, 1):
            print(f"Resultado {i}:")
            print(f"Título: {res['titulo']}")
            print(f"URL: {res['url']}")
            print(f"Snippet: {res['snippet'][:15000]}...\n")  # Muestra primeros 150 caracteres
    else:
        print("No se encontraron resultados.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
