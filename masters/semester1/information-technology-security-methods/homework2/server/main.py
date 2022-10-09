import json
from typing import Tuple
import ssl
from os.path import exists
from OpenSSL import crypto
import requests
from handler import Handler
from certificate_generate import generate_certificate
from itsmsocket import Socket
from config import CA_CERT, SERVER_CERT, SERVER_KEY, HOSTNAME, PORT

def load_ca_certificate():
    if not exists(CA_CERT):
        raise Exception(f"CA certificate \"{CA_CERT}\" does not exist. Impossible to verify identities!")

    with open(CA_CERT) as cert_file:
        return crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())

def check_certificate_validity(client_certificate: 'crypto.X509', ca_certificate: 'crypto.X509'):
    store = crypto.X509Store()  
    store.add_cert(ca_certificate)  
    ctx = crypto.X509StoreContext(store, client_certificate)
    try:
        ctx.verify_certificate()
    except:
        raise Exception(f"Could not verify that the certificate was given out by \"{ca_certificate.get_subject().commonName}\".")

def check_certificate_revokal(client_certificate: 'crypto.X509'):
    url = "http://localhost:8005/revoked"
    certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, client_certificate).decode("ascii")
    body = json.dumps({"certificate": certificate})
    response = requests.post(url, body).json()

    if response["revoked"]:
        subject = client_certificate.get_subject().commonName
        issuer = client_certificate.get_issuer().commonName
        raise Exception(f"Certificate for \"{subject}\" was revoked by \"{issuer}\"")


def retrieve_certificate(connection: 'ssl.SSLSocket', address: 'Tuple[str, int]', ca_certificate: 'crypto.X509') -> 'crypto.X509':
    try:
        client_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, connection.recv(8192))
    except:
        raise Exception(f"Could not load the certificate provided by \"{address[0]}:{address[1]}\"")

    check_certificate_validity(client_certificate, ca_certificate)
    check_certificate_revokal(client_certificate)

    return client_certificate

def handler(connection: 'ssl.SSLSocket', address: 'Tuple[str, int]', ca_certificate: 'crypto.X509'):
    try: 
        subject = f"{address[0]}:{address[1]}"
        client_certificate = retrieve_certificate(connection, address, ca_certificate)
        subject = client_certificate.get_subject().commonName

        print(f"{subject}: Authenticated")

        handler = Handler(subject, connection, address)
        while not handler.is_finished():
            data = connection.recv(8192).decode("utf-8")
            handler.handle(data)
        
    except Exception as exception:
        connection.write(f"server error: {exception}".encode("utf-8"))
        connection.close()
        print(f"{subject}: {exception}")

def main():
    ca_certificate = load_ca_certificate()

    if not exists(SERVER_CERT) or not exists(SERVER_KEY):
        generate_certificate()

    with Socket(HOSTNAME, PORT) as _socket:
        while True:
            _socket.delegate(ca_certificate, handler)

if __name__ == "__main__":
    main()