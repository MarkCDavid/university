import socket
import ssl

SERVER_CERT = "certs/server.pem"

class Socket:
    def __init__(self, certificate: 'str', hostname: 'str', port: 'int'):
        self.certificate = certificate
        self.hostname = hostname
        self.port = port
        self._socket = Socket.build_socket()
        self._ssl_socket = Socket.build_ssl_socket(self._socket)
        self._ssl_socket.connect((hostname, port))
        self._ssl_socket.send(certificate.encode("utf-8"))
        response = self.receive()

        if response.lower().startswith("server error"):
            raise Exception(f"Server error: {response}")

    @staticmethod
    def build_socket():
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    @staticmethod
    def build_ssl_socket(_socket: 'socket.socket'):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(SERVER_CERT)
        context.check_hostname = False
        return context.wrap_socket(_socket)
         
    def __enter__(self):
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._ssl_socket.__exit__(self, exc_type, exc_value, exc_traceback)
        self._socket.__exit__(self, exc_type, exc_value, exc_traceback)

    def send(self, data: 'str'):
        self._ssl_socket.write(data.encode("utf-8"))

    def receive(self):
        return self._ssl_socket.recv(8192).decode("utf-8")