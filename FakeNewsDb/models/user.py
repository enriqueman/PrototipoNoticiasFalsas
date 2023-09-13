from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[str]
    name: str
    lastname: str
    phone: str
    email: str

