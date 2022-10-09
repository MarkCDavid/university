import json
import threading
from typing import Tuple
import requests
import socket
import ssl
from os.path import exists
from OpenSSL import crypto

from cert import generate_certificate

def retrieve_certificate(connection: 'ssl.SSLSocket', address: 'Tuple[str, int]') -> 'crypto.X509':
    try:
        return crypto.load_certificate(crypto.FILETYPE_PEM, connection.recv(2**16))
    except:
        raise Exception(f"Could not load the certificate provided by \"{address[0]}:{address[1]}\"")

def verify_certificate(client_certificate: 'crypto.X509', ca_certificate: 'crypto.X509'):
    store = crypto.X509Store()  
    store.add_cert(ca_certificate)  

    ctx = crypto.X509StoreContext(store, client_certificate)

    try:
        ctx.verify_certificate()
    except:
        raise Exception(f"Could not verify that the certificate was given out by \"{ca_certificate.get_subject().commonName}\".")


def verify_revocation(client_certificate: 'crypto.X509'):
    url = "http://localhost:8005/revoked"
    certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, client_certificate).decode("ascii")
    body = json.dumps({"certificate": certificate})
    response = requests.post(url, body).json()
    if response["revoked"]:
        raise Exception(f"Certificate for \"{client_certificate.get_subject().commonName}\" was revoked by \"{client_certificate.get_issuer().commonName}\"")

def load_ca_certificate():
    if not exists("ca.crt"):
        raise Exception("CA certificate \"ca.crt\" does not exist. Impossible to verify identities!")

    with open("ca.crt") as cert_file:
        return crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())


def thread_function(connection: 'ssl.SSLSocket', address: 'Tuple[str, int]', ca_certificate: 'crypto.X509'):
    try: 
        client_certificate = retrieve_certificate(connection, address)
        verify_certificate(client_certificate, ca_certificate)
        verify_revocation(client_certificate)
        print(f"User {client_certificate.get_subject().commonName} is valid!")
        connection.close()
    except Exception as exception:
        connection.close()
        print(exception)


def main():
    ca_certificate = load_ca_certificate()

    if not exists("server.pem") or not exists("server.key"):
        generate_certificate()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("server.pem", "server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as _socket:
        _socket.bind(('localhost', 8006))
        _socket.listen(5)
        with context.wrap_socket(_socket, server_side=True) as secure_socket:
            connection, address = secure_socket.accept()
            thread = threading.Thread(target=thread_function, args=(connection, address, ca_certificate))
            thread.start()


if __name__ == "__main__":
    main()