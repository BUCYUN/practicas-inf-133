import requests

# URL del servidor RESTful para animales del zoológico
url = "http://localhost:8000/"

# GET para obtener todos los animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("Animales:")
print(get_response.text)

# POST para agregar un nuevo animal
ruta_post = url + "animales"
nuevo_animal = {
    "especie": "Leon",
    "nombre": "Leo",
    "genero": "Masculino",
    "edad": 5,
    "peso": 180,
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_animal)
print("\nNuevo animal agregado:")
print(post_response.text)

# GET filtrando por especie con query params
ruta_get_especie = url + "animales?especie=Leon"
get_response = requests.request(method="GET", url=ruta_get_especie)
print("\nAnimales de la especie Leon:")
print(get_response.text)

# GET filtrando por género con query params
ruta_get_genero = url + "animales?genero=Masculino"
get_response = requests.request(method="GET", url=ruta_get_genero)
print("\nAnimales de género Masculino:")
print(get_response.text)

# PUT para actualizar la información de un animal
ruta_put = url + "animales/1"
datos_actualizados = {
    "nombre": "Leon Actualizado",
    "edad": 6,
    "peso": 190,
}
put_response = requests.request(method="PUT", url=ruta_put, json=datos_actualizados)
print("\nAnimal actualizado:")
print(put_response.text)

# DELETE para eliminar un animal
ruta_delete = url + "animales/2"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print("\nAnimal eliminado:")
print(delete_response.text)

# GET para obtener todos los animales
ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print("\nAnimales:")
print(get_response.text)
