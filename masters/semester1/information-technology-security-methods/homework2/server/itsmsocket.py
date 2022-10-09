import socket
import ssl
import threading
from OpenSSL import crypto

from config import SERVER_CERT, SERVER_KEY

class Socket:
    def __init__(self, hostname: 'str', port: 'int'):
        self.hostname = hostname
        self.port = port
        self._socket = Socket.build_socket(hostname, port)
        self._ssl_socket = Socket.build_ssl_socket(self._socket)

    @staticmethod
    def build_socket(hostname: 'str', port: 'int'):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        _socket.bind((hostname, port))
        _socket.listen(5)
        return _socket

    @staticmethod
    def build_ssl_socket(_socket: 'socket.socket'):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(SERVER_CERT, SERVER_KEY)
        return context.wrap_socket(_socket, server_side=True)
         
    def __enter__(self):
        return self
     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._ssl_socket.__exit__(self, exc_type, exc_value, exc_traceback)
        self._socket.__exit__(self, exc_type, exc_value, exc_traceback)

    def delegate(self, ca_certificate: 'crypto.X509', handler):
        connection, address = self._ssl_socket.accept()
        thread = threading.Thread(target=handler, args=(connection, address, ca_certificate))
        thread.start()

    def send(self, data: 'str'):
        self._ssl_socket.write(data.encode("utf-8"))

    def receive(self):
        return self._ssl_socket.recv(8192).decode("utf-8")
