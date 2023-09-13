from typing import Optional
from pydantic import BaseModel

class Tweet(BaseModel):
    id: Optional[str]
    id_autor: str
    tweet_id: str
    text: str
    date_of_publication: str
    retweet_count: str
    reply_count: str
    like_count: str
    quote_count: str
    bookmark_count: str
    impression_count: str
    verasidad: str

    