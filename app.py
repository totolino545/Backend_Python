from flask import Flask, request, jsonify
from traductor import Traducir
from metadata import Metadatos
app = Flask(__name__)
traductor = Traducir()  # Instancia correcta del traductor
metadata = Metadatos()  # Instancia correcta de los metadatos

@app.route('/')
@app.route('/hello')
def hello():
    return "Hello Python!"

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

if __name__ == '__main__':
    app.run(host='localhost', port=4449, debug=True)