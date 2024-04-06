from zeep import Client

x=3
y=5

client = Client('http://localhost:8000')

resultado_suma = client.service.Sumar(x, y)
print("Suma:", resultado_suma)

resultado_resta = client.service.Restar(x, y)
print("Resta:", resultado_resta)

resultado_multiplicacion = client.service.Multiplicar(x, y)
print("Multiplicacion:", resultado_multiplicacion)

resultado_division = client.service.Dividir(x, y)
print("Division:", resultado_division)