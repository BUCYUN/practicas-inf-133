import requests

base_url = 'http://localhost:8000/pacientes'
headers = {'Content-type': 'application/json'}

# Crear un paciente
nuevo_paciente = {
    'ci': '1234567',
    'nombre': 'Juan',
    'apellido': 'Perez',
    'edad': 30,
    'genero': 'Masculino',
    'diagnostico': 'Diabetes',
    'doctor': 'Dr. Pedro Perez'
}
response = requests.post(base_url, json=nuevo_paciente, headers=headers)
print("Crear un paciente:", response.json())

# Listar todos los pacientes
response = requests.get(base_url)
print("Listar todos los pacientes:", response.json())

# Buscar pacientes por CI
ci = '1234567'
response = requests.get(f'{base_url}/{ci}')
print("Buscar paciente por CI:", response.json())

# Listar a los pacientes que tienen diagnóstico de `Diabetes`
diagnostico = 'Diabetes'
response = requests.get(f'{base_url}/?diagnostico={diagnostico}')
print("Listar pacientes con diagnóstico Diabetes:", response.json())

# Listar a los pacientes que atiende el Doctor `Pedro Pérez`
doctor = 'Dr. Pedro Perez'
response = requests.get(f'{base_url}/?doctor={doctor}')
print("Listar pacientes atendidos por Dr. Pedro Perez:", response.json())

# Actualizar la información de un paciente
ci = '1234567'
nuevos_datos = {
    'nombre': 'Juan Carlos',
    'diagnostico': 'Hipertension'
}
response = requests.put(f'{base_url}/{ci}', json=nuevos_datos, headers=headers)
print("Actualizar información de un paciente:", response.json())

# Eliminar un paciente
response = requests.delete(f'{base_url}/{ci}')
print("Eliminar un paciente:", response.json())


# Listar todos los pacientes
response = requests.get(base_url)
print("Listar todos los pacientes:", response.json())