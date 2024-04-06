import requests

# Define la URL base del servidor
BASE_URL = 'http://localhost:8000/mensajes'

# GET obtener todos los mensajes
response = requests.get(BASE_URL)
print("Todos los mensajes:", response.text)

# POST crear un nuevo mensaje
new_message = {"content": "Este es un nuevo mensaje"}
response = requests.post(BASE_URL, json=new_message)
created_message = response.json()
print("Mensaje creado:", created_message)

# Obtener el ID del mensaje creado
message_id = created_message['id']

# GET obtener un mensaje por ID
response = requests.get(f"{BASE_URL}/{message_id}")
print("Mensaje por ID:", response.json())

# PUT actualizar un mensaje
updated_message = {"content": "Este mensaje ha sido actualizado"}
response = requests.put(f"{BASE_URL}/{message_id}", json=updated_message)
print("Mensaje actualizado:", response.json())

# DELETE eliminar un mensaje
response = requests.delete(f"{BASE_URL}/{message_id}")
print("Respuesta de eliminación:", response.json())
