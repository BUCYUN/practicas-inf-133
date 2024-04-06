import requests

url = "http://localhost:8000/"
# GET obtener a todos los pacientes por la ruta /pacientes
ruta_get = url + "pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print("Mostrar todos los pacientes")
print(get_response.text + "\n")

diagnostico = "Diabetes"
doctor = "Pedro Perez"
ci = "1001"

# POST agrega un nuevo paciente por la ruta /pacientes
ruta_post = url + "pacientes"
nuevo_paciente = {
    "ci":"1000",
    "nombre": "Juan",
    "apellido": "Gonsalez",
    "edad": 30,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_paciente)
print ("Agregar un nuevo paciente")
print(post_response.text + "\n")

# GET filtrando por diagnóstico 
ruta_get_diagnostico = url + f"pacientes?diagnostico={diagnostico}"
get_diagnostico_response = requests.request(method="GET", url=ruta_get_diagnostico)
print ("Mostrar Pacientes Por su diagnostico")
print(get_diagnostico_response.text + "\n")

# GET filtrando por doctor 
ruta_get_doctor = url + f"pacientes?doctor={doctor}"
get_doctor_response = requests.request(method="GET", url=ruta_get_doctor)
print ("Mostrar Pacientes Por El Doctor")
print(get_doctor_response.text +"\n")

# GET buscando por CI
ruta_get_ci = url + f"pacientes/?ci={ci}"
get_ci_response = requests.request(method="GET", url=ruta_get_ci)
print("Mostrar Pacientes Por El CI") 
print(get_ci_response.text + "\n")

# PUT actualizar información de un paciente
ruta_put = url + f"pacientes/{ci}"
datos_actualizados = {
    "diagnostico": "Hipertensión"
}
put_response = requests.request(method="PUT", url=ruta_put, json=datos_actualizados)
print("Actualizar información de un paciente")
print(put_response.text + "\n")

# DELETE eliminar un paciente
ruta_delete = url + f"pacientes/{ci}"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print(delete_response.text + "\n")