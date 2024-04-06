import requests

url = "http://localhost:8000/partidas"

for _ in range(5):
    nueva_partida = {
        "elemento":"piedra"
    }
    response = requests.post(url=url, json=nueva_partida)
    print("Nueva partida:")
    print(response.json())

# Listar partidas ganadas
resultado = "gano"
response = requests.get(f"{url}?resultado={resultado}")
print("\nPartidas ganadas:")
print(response.json())

# Listar partidas perdidas
resultado = "perdio"
response = requests.get(f"{url}?resultado={resultado}")
print("\nPartidas perdidas:")
print(response.json())

resultado = "empate"
response = requests.get(f"{url}?resultado={resultado}")
print("\nPartidas empatadas:")
print(response.json())