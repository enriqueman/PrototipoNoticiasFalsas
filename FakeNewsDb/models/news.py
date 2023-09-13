from typing import Optional
from pydantic import BaseModel

class News(BaseModel):
    id: Optional[str]
    title: str
    body: str
    type: str
    source: str
    date: str
    link: str
