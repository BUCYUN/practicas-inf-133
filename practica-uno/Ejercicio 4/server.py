from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Base de datos simulada de pacientes
pacientes = {}


# Producto: Paciente
class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.edad = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None

    def __str__(self):
        return f"ci: {self.ci}, nombre: {self.nombre}, apellido: {self.apellido}, edad: {self.edad}, genero: {self.genero}, diagnostico: {self.diagnostico}, doctor: {self.doctor}"


# Builder: Constructor de pacientes
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()

    def set_ci(self, ci):
        self.paciente.ci = ci

    def set_nombre(self, nombre):
        self.paciente.nombre = nombre

    def set_apellido(self, apellido):
        self.paciente.apellido = apellido

    def set_edad(self, edad):
        self.paciente.edad = edad

    def set_genero(self, genero):
        self.paciente.genero = genero

    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico

    def set_doctor(self, doctor):
        self.paciente.doctor = doctor

    def get_paciente(self):
        return self.paciente


# Director: Hospital
class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def registrar_paciente(self, ci, nombre, apellido, edad, genero, diagnostico, doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_edad(edad)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()
    
class PacienteService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)
        
    def registrar_paciente(self, post_data):
        ci = post_data.get('ci', None)
        nombre = post_data.get('nombre', None)
        apellido = post_data.get('apellido', None)
        edad = post_data.get('edad', None)
        genero = post_data.get('genero', None)
        diagnostico = post_data.get('diagnostico', None)
        doctor = post_data.get('doctor', None)

        paciente = self.hospital.registrar_paciente(ci, nombre, apellido, edad, genero, diagnostico, doctor)
        pacientes[ci] = paciente
        return paciente

    def listar_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}

    def buscar_paciente_por_ci(self, ci):
        if ci in pacientes:
            return pacientes[ci]
        else:
            return None

    def buscar_pacientes_por_diagnostico(self, diagnostico):
        return [paciente for paciente in pacientes.values() if paciente.diagnostico == diagnostico]

    def buscar_pacientes_por_doctor(self, doctor):
        return [paciente for paciente in pacientes.values() if paciente.doctor == doctor]

    def actualizar_paciente(self, ci, post_data):
        if ci in pacientes:
            paciente = pacientes[ci]
            nombre = post_data.get("nombre", None)
            apellido = post_data.get("apellido", None)
            edad = post_data.get("edad", None)
            genero = post_data.get("genero", None)
            diagnostico = post_data.get("diagnostico", None)
            doctor = post_data.get("doctor", None)
            if nombre:
                paciente.nombre = nombre
            if apellido:
                paciente.apellido = apellido
            if edad:
                paciente.edad = edad
            if genero:
                paciente.genero = genero
            if diagnostico:
                paciente.diagnostico = diagnostico
            if doctor:
                paciente.doctor = doctor
            return paciente
        else:
            return None

    def eliminar_paciente(self, ci):
        if ci in pacientes:
            return pacientes.pop(ci)
        else:
            return None


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


# Manejador de solicitudes HTTP
class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = PacienteService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            if self.path == "/pacientes":
                data = HTTPDataHandler.handle_reader(self)
                response_data = self.controller.registrar_paciente(data)
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
        except Exception as e:
            HTTPDataHandler.handle_response(self, 500, {"Error": str(e)})

    def do_GET(self):
        try:   
            if self.path == "/pacientes":
                response_data = self.controller.listar_pacientes()
                HTTPDataHandler.handle_response(self, 200, response_data)
            elif self.path.startswith("/pacientes/"):
                ci = self.path.split("/")[2]
                response_data = self.controller.buscar_paciente_por_ci(ci)
                if response_data:
                    HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
            elif "?" in self.path:
                query_params = HTTPDataHandler.parse_query_params(self.path.split("?")[-1])
                if "diagnostico" in query_params:
                    diagnostico = query_params["diagnostico"]
                    response_data = [paciente.__dict__ for paciente in self.controller.buscar_pacientes_por_diagnostico(diagnostico)]
                    HTTPDataHandler.handle_response(self, 200, response_data)
                elif "doctor" in query_params:
                    doctor = query_params["doctor"]
                    response_data = [paciente.__dict__ for paciente in self.controller.buscar_pacientes_por_doctor(doctor)]
                    HTTPDataHandler.handle_response(self, 200, response_data)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"Error": "Parámetros de consulta no válidos"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
        except Exception as e:
            HTTPDataHandler.handle_response(self, 500, {"Error": str(e)})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[2]
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.actualizar_paciente(ci, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = self.path.split("/")[2]
            deleted_paciente = self.controller.eliminar_paciente(ci)
            if deleted_paciente:
                HTTPDataHandler.handle_response(self, 200, {"message": "Paciente eliminado exitosamente"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
