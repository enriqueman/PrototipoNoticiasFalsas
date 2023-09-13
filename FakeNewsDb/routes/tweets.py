from fastapi import APIRouter, status, Response
from models.tweet import Tweet
from config.db import conn
from schemas.tweet import serializeDict, tweetsEntity, serializeList, tweetEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


router = APIRouter()

@router.get('/tweets', response_model=list[Tweet], tags=["tweets"])
async def find_all_tweets():
    return tweetsEntity(conn.local.tweet.find())

@router.post('/tweets', response_model=Tweet, tags=["tweets"])
async def create_tweet(tweet: Tweet):
    result = conn.local.tweet.insert_one(dict(tweet))
    tweet_id = result.inserted_id # obtenemos el id del documento insertado
    return serializeDict(conn.local.tweet.find_one({"_id":tweet_id}))

@router.put("/tweets/{id}", response_model=Tweet, tags=["tweets"])
async def update_tweet(id: str, tweet: Tweet):
    conn.local.tweet.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(tweet)
    })
    return serializeDict(conn.local.tweet.find_one({"_id":ObjectId(id)}))

@router.delete("/tweets/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tweets"])
async def delete_tweet(id: str):
     conn.local.tweet.find_one_and_delete({
        "_id": ObjectId(id)
    })
     return Response(status_code=HTTP_204_NO_CONTENT)