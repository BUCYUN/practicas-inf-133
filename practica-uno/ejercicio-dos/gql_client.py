import requests

# Definir la URL del servidor GraphQL con la ruta /graphql
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple para obtener todas las plantas
query_lista = """
{
    plants {
        id
        nombreComun
        especies
        edadMeses
        alturaCm
        frutos
    }
}
"""

response = requests.post(url, json={'query': query_lista})
print(response.text)

# Definir la consulta GraphQL con parámetros para buscar plantas por especie
query_buscar_especie = """
{
    plantsByEspecies(especies: "Rosa spp.") {
        id
        nombreComun
        especies
        edadMeses
        alturaCm
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_buscar_especie})
print(response.text)

# Definir la consulta GraphQL para buscar plantas que tienen frutos
query_buscar_frutos = """
{
    fruitPlants {
        id
        nombreComun
        especies
        edadMeses
        alturaCm
        frutos
    }
}
"""
response = requests.post(url, json={'query': query_buscar_frutos})
print(response.text)

# Definir la consulta GraphQL para crear una nueva planta
query_crear_planta = """
mutation {
    createPlant(
        nombreComun: "Nueva planta",
        especies: "Especie nueva",
        edadMeses: 10,
        alturaCm: 50,
        frutos: false
    ) {
        plant {
            id
            nombreComun
            especies
            edadMeses
            alturaCm
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': query_crear_planta})
print(response.text)

# Definir la consulta GraphQL para actualizar una planta
query_actualizar_planta = """
mutation {
    updatePlant(
        id: 1,
        nombreComun: "Rosa actualizada",
        especies: "Rosa spp.",
        edadMeses: 7,
        alturaCm: 35,
        frutos: true
    ) {
        plant {
            id
            nombreComun
            especies
            edadMeses
            alturaCm
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': query_actualizar_planta})
print(response.text)

# Definir la consulta GraphQL para eliminar una planta
query_eliminar_planta = """
mutation {
    deletePlant(id: 2) {
        plant {
            id
            nombreComun
            especies
            edadMeses
            alturaCm
            frutos
        }
    }
}
"""
response = requests.post(url, json={'query': query_eliminar_planta})
print(response.text)


