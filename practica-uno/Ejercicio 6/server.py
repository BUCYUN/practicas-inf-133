from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

animals = {}


class Animal:
    def __init__(self, tipo, especie, nombre, genero, edad, peso):
        self.tipo = tipo
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso


class Mamifero(Animal):
    def __init__(self, especie, nombre, genero, edad, peso):
        super().__init__("mamifero", especie, nombre, genero, edad, peso)


class Ave(Animal):
    def __init__(self, especie, nombre, genero, edad, peso):
        super().__init__("ave", especie, nombre, genero, edad, peso)


class Reptil(Animal):
    def __init__(self, especie, nombre, genero, edad, peso):
        super().__init__("reptil", especie, nombre, genero, edad, peso)


class Anfibio(Animal):
    def __init__(self, especie, nombre, genero, edad, peso):
        super().__init__("anfibio", especie, nombre, genero, edad, peso)


class Pez(Animal):
    def __init__(self, especie, nombre, genero, edad, peso):
        super().__init__("pez", especie, nombre, genero, edad, peso)


class AnimalFactory:
    @staticmethod
    def create_animal(tipo, especie, nombre, genero, edad, peso):
        if tipo == "mamifero":
            return Mamifero(especie, nombre, genero, edad, peso)
        elif tipo == "ave":
            return Ave(especie, nombre, genero, edad, peso)
        elif tipo == "reptil":
            return Reptil(especie, nombre, genero, edad, peso)
        elif tipo == "anfibio":
            return Anfibio(especie, nombre, genero, edad, peso)
        elif tipo == "pez":
            return Pez(especie, nombre, genero, edad, peso)
        else:
            return ValueError("Tipo de animal no existente")


class ZooService:
    def __init__(self):
        self.factory = AnimalFactory()

    def add_animal(self, data):
        tipo = data.get("tipo", None)
        especie = data.get("especie", None)
        nombre = data.get("nombre", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)

        animal = self.factory.create_animal(tipo, especie, nombre, genero, edad, peso)
        animals[len(animals) + 1] = animal
        return vars(animal)

    def list_animals(self):
        return {index: vars(animal) for index, animal in animals.items()}

    def search_animals_by_especie(self, especie):
        return {index: vars(animal) for index, animal in animals.items() if animal.especie == especie}

    def search_animals_by_genero(self, genero):
        return {index: vars(animal) for index, animal in animals.items() if animal.genero == genero}

    def update_animal(self, animal_id, data):
        if animal_id in animals:
            animal = animals[animal_id]
            for key, value in data.items():
                setattr(animal, key, value)
            return vars(animal)
        else:
            return None

    def delete_animal(self, animal_id):
        if animal_id in animals:
            del animals[animal_id]
            return {"Echo": "Animal Eliminado"}
        else:
            return None


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ZooRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoo_service = ZooService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animals":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"error": "Ruta no Encontrada"})

    def do_GET(self):
        if self.path == "/animals":
            response_data = self.zoo_service.list_animals()
            HTTPDataHandler.handle_response(self, 200, response_data)
        elif "?" in self.path:
            query_params = parse_qs(self.path.split("?")[-1])
            if "especie" in query_params:
                especie = query_params["especie"][0]
                response_data = self.zoo_service.search_animals_by_especie(especie)
                HTTPDataHandler.handle_response(self, 200, response_data)
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                response_data = self.zoo_service.search_animals_by_genero(genero)
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Parámetros de consulta no válidos"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"error": "Route not found"})

    def do_PUT(self):
        if self.path.startswith("/animals/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"error": "Animal no Encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"error": "Route no Encontrado"})

    def do_DELETE(self):
        if self.path.startswith("/animals/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoo_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"error": "Animal no Encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"error": "Route no Encontrado"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZooRequestHandler)
        print("Iniciando servidor HTTP en el puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
