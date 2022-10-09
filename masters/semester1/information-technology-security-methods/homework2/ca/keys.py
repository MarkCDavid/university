import random
from database import Certificates, RevokedCertificates

import hashlib
from hashids import Hashids
from OpenSSL import crypto

class CertificateGenerator:

    CERT_PATH = "certs/ca.crt"
    KEY_PATH = "certs/ca.key"

    def generate_ca_certificate(self, subject: 'str'):
        ca_key = crypto.PKey()
        ca_key.generate_key(crypto.TYPE_RSA, 2048)

        ca_cert = crypto.X509()
        ca_cert.set_version(2)
        ca_cert.set_serial_number(self.generate_serial())

        ca_subj = ca_cert.get_subject()
        ca_subj.commonName = subject

        ca_cert.add_extensions([
            crypto.X509Extension("basicConstraints".encode("ascii"), False, "CA:TRUE".encode("ascii")),
            crypto.X509Extension("keyUsage".encode("ascii"), False, "keyCertSign, cRLSign".encode("ascii")),
        ])

        ca_cert.set_issuer(ca_subj)
        ca_cert.set_pubkey(ca_key)

        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

        ca_cert.sign(ca_key, 'sha256')

        return ca_cert, ca_key

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
        cert_path = CertificateGenerator.CERT_PATH if cert_path is None else cert_path
        key_path = CertificateGenerator.KEY_PATH if key_path is None else key_path

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
    cert, key = cg.generate_ca_certificate("ITSM CA")
    
    with open(CertificateGenerator.CERT_PATH, "wb") as file:
        file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(CertificateGenerator.KEY_PATH, "wb") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

if __name__ == "__main__":
    main()