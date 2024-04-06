from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

animales = [
{
    "id":1,
    "especie": "Elefante",
    "nombre": "Dumbo",
    "genero": "Macho",
    "edad": 10,
    "peso": 5000
},{
    "id":2,
    "especie": "Aguila",
    "nombre": "Thunder",
    "genero": "Hembra",
    "edad": 8,
    "peso": 6
},{
    "id":3,
    "especie": "Cocodrilo",
    "nombre": "Snappy",
    "genero": "Macho",
    "edad": 15,
    "peso": 700
}]

class AnimalesService:

    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )

    @staticmethod
    def filter_animals_by_species(species):
        return [
            animal for animal in animales if animal["especie"] == species
        ]

    @staticmethod
    def filter_animals_by_gender(gender):
        return [
            animal for animal in animales if animal["genero"] == gender
        ]

    @staticmethod
    def add_animal(data):
        data["id"] = len(animales) + 1
        animales.append(data)
        return animales

    @staticmethod
    def update_animal(id, data):
        animal = AnimalesService.find_animal(id)
        if animal:
            animal.update(data)
            return animales
        else:
            return None

    @staticmethod
    def delete_animal(id):
        for i, animal in enumerate(animales):
            if animal["id"] == id:
                animales.pop(i)
                return animales
        return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                species = query_params["especie"][0]
                animals_filtered = AnimalesService.filter_animals_by_species(species)
                if animals_filtered:
                    HTTPResponseHandler.handle_response(
                        self, 200, animals_filtered
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                gender = query_params["genero"][0]
                animals_filtered = AnimalesService.filter_animals_by_gender(gender)
                if animals_filtered:
                    HTTPResponseHandler.handle_response(
                        self, 200, animals_filtered
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, animales)
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = AnimalesService.find_animal(id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, [animal])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animals = AnimalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animals)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            animals = AnimalesService.update_animal(id, data)
            if animals:
                HTTPResponseHandler.handle_response(self, 200, animals)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animals = AnimalesService.delete_animal(id)
            if animals:
                HTTPResponseHandler.handle_response(self, 200, animals)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
