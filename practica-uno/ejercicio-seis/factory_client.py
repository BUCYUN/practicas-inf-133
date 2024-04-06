import requests
import json

url = "http://localhost:8000/animals"
headers = {"Content-Type": "application/json"}

# POST /animals
nuevo_animal_data_1 = {
    "tipo": "mamifero",
    "especie": "Elefante",
    "nombre": "Dumbo",
    "genero": "Macho",
    "edad": 10,
    "peso": 5000
}

nuevo_animal_data_2 = {
    "tipo": "ave",
    "especie": "Aguila",
    "nombre": "Thunder",
    "genero": "Hembra",
    "edad": 8,
    "peso": 6
}

nuevo_animal_data_3 = {
    "tipo": "reptil",
    "especie": "Cocodrilo",
    "nombre": "Snappy",
    "genero": "Macho",
    "edad": 15,
    "peso": 700
}

response = requests.post(url=url, json=nuevo_animal_data_1, headers=headers)
print(response.json())

response = requests.post(url=url, json=nuevo_animal_data_2, headers=headers)
print(response.json())

response = requests.post(url=url, json=nuevo_animal_data_3, headers=headers)
print(response.json())

# listar todos los animales
response = requests.get(url=url)
print(response.json())

# mostrar animal por especie
especie = "Cocodrilo"
response = requests.get(f"{url}?especie={especie}")
print(response.json())

# mostrar animal por genero
genero = "Macho"
response = requests.get(f"{url}?genero={genero}")
print(response.json())

# actualizar animal
animal_id_to_update = 1
updated_animal_data = {
    "nombre": "Elefante Actualizado",
    "edad": 6
}
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data, headers=headers)
print("Animal actualizado:", response.json())

# eliminar animal
animal_id_to_delete = 2
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Animal eliminado:", response.json())

# listar todos los animales actualizado
response = requests.get(url=url)
print(response.json())

