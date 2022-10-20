import json
from typing import Tuple
import ssl
from os.path import exists
from OpenSSL import crypto
import requests
from certificate_generate import generate_certificate
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
    url = "https://ca.itsm.local:8005/revoked"
    certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, client_certificate).decode("ascii")
    body = json.dumps({"certificate": certificate})
    response = requests.post(url, body, verify=False).json()

    if response["revoked"]:
        subject = client_certificate.get_subject().commonName
        issuer = client_certificate.get_issuer().commonName
        raise Exception(f"Certificate for \"{subject}\" was revoked by \"{issuer}\"")


def check_certificate(certificate: 'str', ca_certificate: 'crypto.X509') -> 'crypto.X509':
    try:
        client_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
    except:
        raise Exception(f"Could not load the certificate.")

    check_certificate_validity(client_certificate, ca_certificate)
    check_certificate_revokal(client_certificate)

    return client_certificate