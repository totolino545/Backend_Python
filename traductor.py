from googletrans import Translator

class Traducir:
    def __init__(self):
        self.translator = Translator()

    def traducir_texto(self, texto, idioma_destino='es'):
        try:
            if not texto:  # Ahora recibe correctamente el parámetro
                return {'error': 'Texto vacío recibido'}, 400
                
            traduccion = self.translator.translate(texto, dest=idioma_destino)
            return {'texto_traducido': traduccion.text}, 200
            
        except Exception as e:
            print(f"Error en traducción: {str(e)}")
            return {'error': 'Error interno en la traducción'}, 500