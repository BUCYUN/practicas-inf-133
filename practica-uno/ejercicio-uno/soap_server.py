from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def Sumar(x, y):
    return x + y

def Restar(x, y):
    return x - y

def Multiplicar(x, y):
    return x * y

def Dividir(x, y):
    if y == 0:
        return "Error: No se puede dividir por cero"
    else:
        return x / y

dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Sumar",
    Sumar,
    returns={"resultado": int},
    args={"x": int, "y": int},
)

dispatcher.register_function(
    "Restar",
    Restar,
    returns={"resultado": int},
    args={"x": int, "y": int},
)

dispatcher.register_function(
    "Multiplicar",
    Multiplicar,
    returns={"resultado": int},
    args={"x": int, "y": int},
)

dispatcher.register_function(
    "Dividir",
    Dividir,
    returns={"resultado": float},
    args={"x": int, "y": int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
