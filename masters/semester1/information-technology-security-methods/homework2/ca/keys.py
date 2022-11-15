import random
from database import Certificates, RevokedCertificates

import hashlib
from hashids import Hashids
from OpenSSL import crypto

class CertificateGenerator:

    CA_CERT_PATH = "certs/ca.crt"
    CA_KEY_PATH = "certs/ca.key"
    API_CERT_PATH = "certs/api.crt"
    API_KEY_PATH = "certs/api.key"

    def generate_ca_certificate(self, ca_subject: 'str', api_subject: 'str'):
        ca_key = crypto.PKey()
        ca_key.generate_key(crypto.TYPE_RSA, 2048)

        ca_cert = crypto.X509()
        ca_cert.set_version(2)
        ca_cert.set_serial_number(self.generate_serial())

        ca_subj = ca_cert.get_subject()
        ca_subj.commonName = ca_subject

        ca_cert.add_extensions([
            crypto.X509Extension("basicConstraints".encode("ascii"), False, "CA:TRUE".encode("ascii")),
            crypto.X509Extension("keyUsage".encode("ascii"), False, "keyCertSign, cRLSign".encode("ascii")),
        ])

        ca_cert.set_issuer(ca_subj)
        ca_cert.set_pubkey(ca_key)

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

        ca_cert.sign(ca_key, 'sha256')

        api_key = crypto.PKey()
        api_key.generate_key(crypto.TYPE_RSA, 2048)

        api_cert = crypto.X509()
        api_cert.set_version(2)
        api_cert.set_serial_number(self.generate_serial())

        api_subj = api_cert.get_subject()
        api_subj.commonName = api_subject

        api_cert.add_extensions([
            crypto.X509Extension("subjectAltName".encode("ascii"), False, f"DNS:{api_subject}".encode("ascii")),
            crypto.X509Extension("keyUsage".encode("ascii"), False, "digitalSignature, keyEncipherment".encode("ascii")),
        ])

        api_cert.set_issuer(ca_subj)
        api_cert.set_pubkey(api_key)

        api_cert.gmtime_adj_notBefore(0)
        api_cert.gmtime_adj_notAfter(10*365*24*60*60)

        api_cert.sign(ca_key, 'sha256')

        return ca_cert, ca_key, api_cert, api_key

    def generate_client_certificate(self, subject: 'str', ca_cert: 'crypto.X509', ca_key: 'crypto.PKey'):
        self.ensure_unique_subject(subject)
        client_key = crypto.PKey()
        client_key.generate_key(crypto.TYPE_RSA, 2048)

        client_cert = crypto.X509()
        client_cert.set_version(2)
        client_cert.set_serial_number(self.generate_serial())

        client_subj = client_cert.get_subject()
        client_subj.commonName = subject

        client_cert.set_issuer(ca_cert.get_subject())
        client_cert.set_pubkey(client_key)
        
        client_cert.gmtime_adj_notBefore(0)
        client_cert.gmtime_adj_notAfter(10*365*24*60*60)
        
        client_cert.sign(ca_key, 'sha256')

        return client_cert

    def sign_server_certificate(self, certificate_signing_request: 'str', ca_cert: 'crypto.X509', ca_key: 'crypto.PKey'):
        
        csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, certificate_signing_request)
        self.ensure_unique_subject(csr.get_subject().commonName)

        client_cert = crypto.X509()
        client_cert.set_version(2)
        client_cert.set_serial_number(self.generate_serial())
        
        client_cert.set_subject(csr.get_subject())
        client_cert.set_issuer(ca_cert.get_subject())
        client_cert.set_pubkey(csr.get_pubkey())

        client_cert.add_extensions([
            crypto.X509Extension("subjectAltName".encode("ascii"), False, f"DNS:{csr.get_subject().commonName}".encode("ascii")),
        ])

        client_cert.gmtime_adj_notBefore(0)
        client_cert.gmtime_adj_notAfter(10*365*24*60*60)

        client_cert.sign(ca_key, 'sha256')

        return client_cert
        

    def revoke_client_certificate(self, subject: 'str', key: 'str'):
        try:
            certificate: Certificates = Certificates.get(Certificates.subject==subject)
            hash = self.hash_key(subject, key)
            print(hash)
            print(certificate.keyhash)
            if certificate.keyhash != hash:
                raise Exception()

            RevokedCertificates.create(serial=certificate.serial).save()
            certificate.delete_instance()

        except:
            raise Exception(f"Recovery key '{key}' invalid for subject '{subject}'!")
        
    def load_ca_certificates(self, cert_path: 'str' = None, key_path: 'str' = None):
        cert_path = CertificateGenerator.CA_CERT_PATH if cert_path is None else cert_path
        key_path = CertificateGenerator.CA_KEY_PATH if key_path is None else key_path

        with open(cert_path, "rb") as file:
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, file.read())

        with open(key_path, "rb") as file:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, file.read())

        return ca_cert, ca_key

    def generate_recovery_key(self, client_cert: 'crypto.X509'):
        key = Hashids(min_length=256).encode(random.randint(1, 10**256))
        hash = self.hash_key(client_cert.get_subject().commonName, key)
        return key, hash

    def hash_key(self, subject: 'str', key: 'str'):
        return hashlib.sha256(f"{subject}{key}".encode('utf-8')).hexdigest()

    def generate_serial(self):
        while True:
            serial = random.randint(50000000,100000000)
            existing_count = Certificates.select().where(Certificates.serial == serial).count()
            if existing_count == 0:
                return serial


    def is_revoked(self, pem_certificate: 'str'):
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, pem_certificate)
        serial = certificate.get_serial_number()
        try:
            RevokedCertificates.get(RevokedCertificates.serial==serial)
        except:
            return False

        return True

    def ensure_unique_subject(self, subject: 'str'):
        existing_count = Certificates.select().where(Certificates.subject==subject).count()
        if existing_count != 0:
            raise Exception(f"Subject name '{subject}' is already taken!")

def main():
    cg = CertificateGenerator()
    ca_cert, ca_key, api_cert, api_key = cg.generate_ca_certificate("ITSM CA", "ca.itsm.local")
    
    with open(CertificateGenerator.CA_CERT_PATH, "wb") as file:
        file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))

    with open(CertificateGenerator.CA_KEY_PATH, "wb") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))

    with open(CertificateGenerator.API_CERT_PATH, "wb") as file:
        file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, api_cert))

    with open(CertificateGenerator.API_KEY_PATH, "wb") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, api_key))

if __name__ == "__main__":
    main()