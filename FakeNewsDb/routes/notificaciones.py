# routes/user.py
from fastapi import APIRouter, status, Response
from models.notificaciones import Notificaciones
from config.dbfirebase import db
from schemas.notificaciones import notificationsEntity
from schemas.user import serializeDict, usersEntity, serializeList, userEntity
from starlette.status import HTTP_204_NO_CONTENT

from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
import os

router = APIRouter()
load_dotenv()

password= os.getenv('PASSWORD')
notificaciones = APIRouter()

@notificaciones.get('/Notificaciones', tags=["Notificaciones"])
async def find_all_notificaciones():
    doc_ref = db.reference('/notificaciones')
    lis=[doc_ref.get()]
    #print(lis)
      # Procesar la respuesta
    processed_response = []
    for item in lis[0].values():
        processed_response.append(item)
    print(type(processed_response))
    return [(processed_response)]

@notificaciones.post('/Notificaciones', response_model=Notificaciones, tags=["Notificaciones"])
async def create_notificaciones(notificaciones: Notificaciones):
    doc_ref = db.reference('/notificaciones')  
    new_data = doc_ref.push(dict(notificaciones)) 
    id = new_data.key  # Obtiene el ID del nuevo dato
    print(id)
    #print(doc_ref.child(id).get())
    return dict(doc_ref.child(id).get())

@notificaciones.put("/Actualizar_Notificaciones/{id}", response_model=Notificaciones, tags=["Notificaciones"])
async def update_user(id: str,notificaciones: Notificaciones):
    ref = db.reference('notificaciones')
    notificacion_ref=ref.child(id)
    notificacion_ref.update(dict(notificaciones))
    return dict(ref.child(id).get())

@notificaciones.delete("/Delete_Notificaciones/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Notificaciones"])
async def delete_user(id: str):
    doc_ref = db.reference('/notificaciones')  
    doc_ref.child(id).delete() 
    return Response(status_code=HTTP_204_NO_CONTENT)


