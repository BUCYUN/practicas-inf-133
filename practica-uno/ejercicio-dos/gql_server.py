from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, List, Schema, Field, Mutation, Boolean

class Plant(ObjectType):
    id = Int()
    nombreComun = String()
    especies = String()
    edadMeses = Int()
    alturaCm = Int()
    frutos = Boolean()

class Query(ObjectType):
    plants = List(Plant)
    plants_by_especies = List(Plant, especies=String())
    fruit_plants = List(Plant)

    def resolve_plants(root, info):
        return plants
    
    def resolve_plants_by_especies(root, info, especies):
        return [plant for plant in plants if plant.especies == especies]

    def resolve_fruit_plants(root, info):
        return [plant for plant in plants if plant.frutos]

class CreatePlant(Mutation):
    class Arguments:
        nombreComun = String()
        especies = String()
        edadMeses = Int()
        alturaCm = Int()
        frutos = Boolean()

    plant = Field(Plant)

    def mutate(root, info, nombreComun, especies, edadMeses, alturaCm, frutos):
        new_plant = Plant(
            id=len(plants) + 1, 
            nombreComun=nombreComun, 
            especies=especies, 
            edadMeses=edadMeses, 
            alturaCm=alturaCm, 
            frutos=frutos
        )
        plants.append(new_plant)

        return CreatePlant(plant=new_plant)

class UpdatePlant(Mutation):
    class Arguments:
        id = Int()
        nombreComun = String()
        especies = String()
        edadMeses = Int()
        alturaCm = Int()
        frutos = Boolean()

    plant = Field(Plant)

    def mutate(root, info, id, nombreComun=None, especies=None, edadMeses=None, alturaCm=None, frutos=None):
        for plant in plants:
            if plant.id == id:
                if nombreComun:
                    plant.nombreComun = nombreComun
                if especies:
                    plant.especies = especies
                if edadMeses:
                    plant.edadMeses = edadMeses
                if alturaCm:
                    plant.alturaCm = alturaCm
                if frutos is not None:
                    plant.frutos = frutos
                return UpdatePlant(plant=plant)
        return None

class DeletePlant(Mutation):
    class Arguments:
        id = Int()

    plant = Field(Plant)

    def mutate(root, info, id):
        for i, plant in enumerate(plants):
            if plant.id == id:
                plants.pop(i)
                return DeletePlant(plant=plant)
        return None

class Mutations(ObjectType):
    create_plant = CreatePlant.Field()
    update_plant = UpdatePlant.Field()
    delete_plant = DeletePlant.Field()

plants = [
    Plant(
        id=1, nombreComun="Rosa", especies="Rosa spp.", edadMeses=6, alturaCm=30, frutos=False
    ),
    Plant(
        id=2, nombreComun="Tomate", especies="Solanum lycopersicum", edadMeses=4, alturaCm=20, frutos=True
    ),
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
