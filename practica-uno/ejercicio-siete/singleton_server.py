import http.server
import json
import random

class Partida:
    def __init__(self, id, elemento):
        self.id = id
        self.elemento = elemento
        self.elemento_servidor = random.choice(["piedra", "papel", "tijera"])
        self.resultado = self.calcular_resultado()

    def calcular_resultado(self):
        if self.elemento == self.elemento_servidor:
            return "empate"
        elif (self.elemento == "piedra" and self.elemento_servidor == "tijera") or \
            (self.elemento == "tijera" and self.elemento_servidor == "papel") or \
            (self.elemento == "papel" and self.elemento_servidor == "piedra"):
            return "gano"
        else:
            return "perdio"

class PartidaService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.partidas = []
        return cls._instance

    def crear_partida(self, elemento):
        id = len(self.partidas) + 1
        partida = Partida(id, elemento)
        self.partidas.append(partida)
        return partida

    def listar_partidas(self, resultado=None):
        if resultado:
            return [partida.__dict__ for partida in self.partidas if partida.resultado == resultado]
        else:
            return [partida.__dict__ for partida in self.partidas]
        
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header('Content-type', 'application/json')
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

class PartidaHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        data = HTTPDataHandler.handle_reader(self)
        elemento = data.get('elemento')
        partida = PartidaService().crear_partida(elemento)
        HTTPDataHandler.handle_response(self, 200, partida.__dict__)

    def do_GET(self):
        if self.path.startswith('/partidas'):
            resultado = None
            if '?' in self.path:
                resultado = self.path.split('=')[-1]
            partidas = PartidaService().listar_partidas(resultado)
            HTTPDataHandler.handle_response(self, 200, partidas)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

def main(server_class=http.server.HTTPServer, handler_class=PartidaHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Iniciando servidor HTTP en puerto {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
