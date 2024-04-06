from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


class MessageHandler:
    def __init__(self):
        self.messages = []

    def create_message(self, content):
        encrypted_content = self.encrypt(content)
        message = {
            "id": len(self.messages) + 1,
            "content": content,
            "encrypted_content": encrypted_content
        }
        self.messages.append(message)
        return message

    def list_messages(self):
        return self.messages

    def get_message_by_id(self, message_id):
        for message in self.messages:
            if message["id"] == message_id:
                return message
        return None

    def update_message(self, message_id, new_content):
        message = self.get_message_by_id(message_id)
        if message:
            message["Mensaje"] = new_content
            message["Mensaje Encriptado"] = self.encrypt(new_content)
            return message
        return None

    def delete_message(self, message_id):
        message = self.get_message_by_id(message_id)
        if message:
            self.messages.remove(message)
            return True
        return False

    def encrypt(self, content):
        encrypted_content = ""
        for char in content:
            if char.isalpha():
                shift = 3
                if char.islower():
                    encrypted_content += chr((ord(char) - 97 + shift) % 26 + 97)
                else:
                    encrypted_content += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                encrypted_content += char
        return encrypted_content


class HTTPResponseHandler:
    @staticmethod
    def set_response(handler, status_code=200, content_type="application/json", body=None):
        handler.send_response(status_code)
        handler.send_header("Content-type", content_type)
        handler.end_headers()

        if body:
            handler.wfile.write(json.dumps(body).encode())


class RESTRequestHandler(BaseHTTPRequestHandler):
    message_handler = MessageHandler()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        if path == "/mensajes":
            messages = self.message_handler.list_messages()
            HTTPResponseHandler.set_response(self, body=messages)
        elif path.startswith("/mensajes/"):
            message_id = int(path.split("/")[2])
            message = self.message_handler.get_message_by_id(message_id)
            if message:
                HTTPResponseHandler.set_response(self, body=message)
            else:
                HTTPResponseHandler.set_response(self, status_code=404, body={"error": "Messaje no Encontrado"})
        else:
            HTTPResponseHandler.set_response(self, status_code=404, body={"error": "No Encontrado"})

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        content = data.get("content")
        if content:
            message = self.message_handler.create_message(content)
            HTTPResponseHandler.set_response(self, status_code=201, body=message)
        else:
            HTTPResponseHandler.set_response(self, status_code=400, body={"error": "Requiere Contenido"})

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        message_id = int(parsed_path.path.split("/")[2])
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        data = json.loads(put_data.decode())
        new_content = data.get("content")
        if new_content:
            updated_message = self.message_handler.update_message(message_id, new_content)
            if updated_message:
                HTTPResponseHandler.set_response(self, body=updated_message)
            else:
                HTTPResponseHandler.set_response(self, status_code=404, body={"error": "Messaje no Encontrado"})
        else:
            HTTPResponseHandler.set_response(self, status_code=400, body={"error": "Requiere Contenido"})

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        message_id = int(parsed_path.path.split("/")[2])
        if self.message_handler.delete_message(message_id):
            HTTPResponseHandler.set_response(self, body={"message": "Messaje Eliminado"})
        else:
            HTTPResponseHandler.set_response(self, status_code=404, body={"error": "Messaje no Encontrado"})

def main(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    main()
