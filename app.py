from flask import Flask, request, jsonify, json
import os
from flask_cors import CORS
from traductor import Traducir
from metadata import Metadatos
from buscador_imagenes import Buscador_Imagenes
from buscador_textos import Buscador_Textos
from buscador_letras import Buscador_Letras
from duckduckgo_search import DDGS


app = Flask(__name__)
CORS(app)  # Esto habilita CORS para toda la app
traductor = Traducir()  # Instancia correcta del traductor
metadata = Metadatos()  # Instancia correcta de los metadatos
buscador = Buscador_Imagenes()  # Instancia correcta del buscador de imágenes
buscador_textos = Buscador_Textos()  # Instancia correcta del buscador de textos
buscador_letras = Buscador_Letras()  # Instancia correcta del buscador de letras

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
def buscar_texto():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({'error': 'Parámetro "texto" requerido'}), 400
    try:
        summary = buscador_textos.buscar_textos(texto, max_resultados=1)
        if not summary:
            return jsonify({'error': 'No se encontraron resultados en la busqueda'}), 404
        return jsonify({'summary': summary})
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/lyrics', methods=['GET'])
def buscar_letras():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Parámetro "query" requerido'}), 400
    try:
        summary = buscador_letras.buscar_letra(query[0], query[1], max_resultados=1)
        if not summary:
            return jsonify({'error': 'No se encontraron resultados en la busqueda'}), 404
        return jsonify({'summary': summary})
    except Exception as e:
        print(f"Error en el servidor: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
