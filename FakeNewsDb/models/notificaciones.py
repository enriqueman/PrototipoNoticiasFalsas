from typing import Optional
from pydantic import BaseModel

class Notificaciones(BaseModel):
    #id: Optional[str]
    titulo: Optional[str]
    texto: str
    fecha: str
    veracidad: str
    autor: str
    notificado: str