from pydantic import BaseModel
from keys import CertificateGenerator 
from database import Certificates
from OpenSSL import crypto

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()
cg = CertificateGenerator()


def _generate_client_certificate(subject: 'str'):
    
        ca_cert, ca_key = cg.load_ca_certificates()
        client_cert = cg.generate_client_certificate(subject, ca_cert, ca_key)
        recovery_key, recovery_hash = cg.generate_recovery_key(client_cert)

        Certificates.create(
            subject=client_cert.get_subject().commonName,
            serial=client_cert.get_serial_number(), 
            keyhash=recovery_hash
        ).save()

        return { 
            "cert_pem": crypto.dump_certificate(crypto.FILETYPE_PEM, client_cert),
            "cert_recovery": recovery_key,
        }

class Generate(BaseModel):
    subject: str

class Recover(BaseModel):
    subject: str
    key: str

class Revoked(BaseModel):
    certificate: str

@app.post("/generate")
def generate_client_certificate(body: 'Generate'):
    try:
        return _generate_client_certificate(body.subject)
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)

@app.post("/recover")
def recover_client_certificate(body: 'Recover'):
    try:
        cg.revoke_client_certificate(body.subject, body.key)
        return _generate_client_certificate(body.subject)
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)

@app.post("/revoked")
def check_certificate_revokal(body: 'Revoked'):
    try:
        return {
            "revoked": cg.is_revoked(body.certificate)
        }
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)
    
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}