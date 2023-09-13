from typing import Optional
from pydantic import BaseModel

class UserTweet(BaseModel):
    id: Optional[str]
    Usuario: str
    id_user: str
    name: str
    location: str
    description: str
    entities: str
    followers_count: str
    friends_count: str
    created_at: str
    listed_count: str
    verified: str
    
    