import socket
import ssl

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("server.pem")
    context.check_hostname = False

    with open("client.pem", "rb") as file:
        certificate = file.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as _socket:
        with context.wrap_socket(_socket) as secure_socket:
            secure_socket.connect(("localhost", 8006))
            secure_socket.send(certificate)
            secure_socket.close()
          

if __name__ == "__main__":
    main()