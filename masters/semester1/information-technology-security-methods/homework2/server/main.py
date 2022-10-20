import random
import json
from pydantic import BaseModel
import uvicorn
from database import Todo

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from certificate import load_ca_certificate, check_certificate
from fastapi import FastAPI
from hashids import Hashids
from fastapi.responses import JSONResponse, Response
from playhouse.shortcuts import model_to_dict

ca_cert = load_ca_certificate()
app = FastAPI()

app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CertifiedBaseModel(BaseModel):
    certificate: str

class Add(CertifiedBaseModel):
    value: str

class Toggle(CertifiedBaseModel):
    id: str

class Delete(CertifiedBaseModel):
    id: str

@app.post("/all")
def all_todos(body: 'CertifiedBaseModel'):
    try:
        client_certificate = check_certificate(body.certificate, ca_cert)
        todos = [model_to_dict(todo) for todo in Todo.select().where(Todo.owner==client_certificate.get_subject().commonName)]
        return JSONResponse(content={'todos': todos})
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)

@app.post("/add")
def add_todo(body: 'Add'):
    try:
        client_certificate = check_certificate(body.certificate, ca_cert)
        id = Hashids(min_length=64).encode(random.randint(1, 10**64))
        
        todo = Todo.create(
            id=id,
            owner=client_certificate.get_subject().commonName,
            value=body.value,
            completed=False
        )
        todo.save()
        return Response()
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)

@app.post("/toggle")
def toggle_todo(body: 'Toggle'):
    try:
        client_certificate = check_certificate(body.certificate, ca_cert)
        todo = _get_todo(body.id, client_certificate)
        todo.completed = not todo.completed
        todo.save()

    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)


@app.post("/delete")
def delete_todo(body: 'Delete'):
    try:
        client_certificate = check_certificate(body.certificate, ca_cert)
        todo = _get_todo(body.id, client_certificate)
        todo.delete_instance()
    except Exception as exception:
        return JSONResponse(content={'reason': str(exception)}, status_code=400)


def _get_todo(id, certificate):
    try:
        return Todo.select().where(
            (Todo.id==id) & 
            (Todo.owner==certificate.get_subject().commonName)).get()
    except:
        raise Exception(f"Todo with id {id} does not exist!")

if __name__ == '__main__':
    uvicorn.run(
        'main:app', port=8006, host='server.itsm.local',
        reload=False,
        ssl_keyfile='./certs/server.key',
        ssl_certfile='./certs/server.pem')