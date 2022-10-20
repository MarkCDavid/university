import json
import requests
from OpenSSL import crypto

def generate_certificate():
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 2048)

    ca_cert = crypto.X509Req()
    ca_cert.set_version(2)

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = "server.itsm.local"

    ca_cert.set_pubkey(ca_key)

    ca_cert.sign(ca_key, 'sha256')

    url = "https://localhost:8005/sign"
    body = json.dumps({"certificate_signing_request": crypto.dump_certificate_request(crypto.FILETYPE_PEM, ca_cert).decode('ascii')})
    response = requests.post(url, body, verify=False)
    response_json = response.json()

    if not response.ok:
        raise Exception(f"Failed to generate a certificate: {response_json['reason']}")
    
    with open("certs/server.pem", "wb") as file:
        file.write(response_json["cert_pem"].encode("utf-8"))

    with open("certs/server.key", "wb") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))

if __name__ == "__main__":
    generate_certificate()
