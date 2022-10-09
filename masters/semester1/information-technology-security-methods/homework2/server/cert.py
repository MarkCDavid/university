from OpenSSL import crypto

def generate_certificate():
    ca_key = crypto.PKey()
    ca_key.generate_key(crypto.TYPE_RSA, 2048)

    ca_cert = crypto.X509()
    ca_cert.set_version(2)

    ca_subj = ca_cert.get_subject()
    ca_subj.commonName = "server1"

    ca_cert.set_issuer(ca_subj)
    ca_cert.set_pubkey(ca_key)

    ca_cert.gmtime_adj_notBefore(0)
    ca_cert.gmtime_adj_notAfter(10*365*24*60*60)

    ca_cert.sign(ca_key, 'sha256')
    
    with open("server.pem", "wb") as file:
        file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, ca_cert))

    with open("server.key", "wb") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, ca_key))

if __name__ == "__main__":
    generate_certificate()