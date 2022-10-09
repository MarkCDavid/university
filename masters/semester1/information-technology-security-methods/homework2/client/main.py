import socket
import ssl
import sys

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("server.pem")
    context.check_hostname = False

    certificate = sys.argv[1]

    with open(certificate, "rb") as file:
        certificate = file.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as _socket:
        with context.wrap_socket(_socket) as secure_socket:
            secure_socket.connect(("localhost", 8007))
            secure_socket.send(certificate)
            print(secure_socket.recv(2**16).decode("utf-8"))
            while True:
                user_input = input()
                secure_socket.write(user_input.encode("utf-8"))
                if user_input == "exit":
                    return
                data = secure_socket.recv(2**16).decode("utf-8")
                print(data)
          

if __name__ == "__main__":
    main()