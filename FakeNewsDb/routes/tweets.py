from fastapi import APIRouter, status, Response
from models.tweet import Tweet
from config.db import conn
from schemas.tweet import serializeDict, tweetsEntity, serializeList, tweetEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
from config.twitter import client, api
import pandas as pd
import json

router = APIRouter()

@router.get('/tweets', response_model=list[Tweet], tags=["tweets"])
async def find_all_tweets():
    return tweetsEntity(conn.local.tweet.find())

# corregir respuesta de peticion
@router.get('/get_user_tweets_id/{id1,numero_resultados}', tags=["tweets"])
async def get_tweets_id_user(id1: int,numero_resultados:int):

    try:
        tweets_test=client.get_users_tweets(
            id=id1,
            expansions=["author_id",
                        "referenced_tweets.id",
                        "referenced_tweets.id.author_id",
                        "in_reply_to_user_id",
                        "geo.place_id", 
                        "entities.mentions.username"
                        ],
            tweet_fields=["created_at",
                          "author_id",
                          "text",
                          "conversation_id",
                          "public_metrics",
                          "context_annotations",
                          "reply_settings",
                          "referenced_tweets",
                          "attachments",
                        ],
                user_fields=["username"],
                max_results=numero_resultados,
            )
        
        data = []
        tweetid=[]
        for tweet in tweets_test.data:
            tweet_data = {
                'id':'null',
                'tweet_id': str(tweet.id),
                'Text': tweet.text,
                'id_autor': str(tweet.author_id),
                'date_of_publication': str(tweet.created_at),
                'verasidad':'por comprobar'
            }
            for key, value in tweet.public_metrics.items():
                tweet_data[key] = value
            data.append(tweet_data)
            #json_data = json.dumps(data)
        conn.local.tweet.insert_many(data)
        #tweetid.extend(result.inserted_ids)
   
        
        
        return 'Hecho'
    except Exception as e:
        menssage=str({'error':e, 'Data':data})
        return menssage
    

#optener tweets por scren name
@router.get('/get_user_tweets_screenname/{screen_name,numero_resultados}', tags=["tweets"])
async def get_tweets_user_screenname(screen_name: str,numero_resultados: int):

    existing_user = conn.local.usertweet.find_one({"Usuario": screen_name})
    if existing_user is not None:
    # El usuario ya existe en la base de datos

        user_id = existing_user["id_user"]
        
    
    else:
        # El usuario no existe en la base de datos, procede a guardar la información del usuario
        usern= '@'+screen_name
        try:
            user = api.get_user(screen_name=usern)
            response={
                'Usuario': str(user.screen_name),
                'id_user':str(user.id),
                'name':str(user.name),
                'location':str(user.location),
                'description':str(user.description),
                'entities':str(user.entities),
                'followers_count':str(user.followers_count),
                'friends_count':str(user.friends_count),
                'created_at':str(user.created_at),
                'listed_count':str(user.listed_count),
                'verified':str(user.verified),
                    }
            conn.local.usertweet.insert_one(response)
            user_id=str(user.id)

            menssage="entro"
        except Exception as e:
            menssage=e
#Consulta de usuarios 
    try:
        tweets_test=client.get_users_tweets(
            id=int(user_id),
            expansions=["author_id",
                        "referenced_tweets.id",
                        "referenced_tweets.id.author_id",
                        "in_reply_to_user_id",
                        "geo.place_id", 
                        "entities.mentions.username"
                        ],
            tweet_fields=["created_at",
                          "author_id",
                          "text",
                          "conversation_id",
                          "public_metrics",
                          "context_annotations",
                          "reply_settings",
                          "referenced_tweets",
                          "attachments",
                        ],
                user_fields=["username"],
                max_results=numero_resultados,
            )
        
        data = []
        tweetid=[]
        for tweet in tweets_test.data:
            tweet_data = {
                'id':'null',
                'tweet_id': str(tweet.id),
                'Text': tweet.text,
                'id_autor': str(tweet.author_id),
                'date_of_publication': str(tweet.created_at),
                'verasidad':'por comprobar'
            }
            for key, value in tweet.public_metrics.items():
                tweet_data[key] = value
            data.append(tweet_data)
            #json_data = json.dumps(data)
        conn.local.tweet.insert_many(data)
        #tweetid.extend(result.inserted_ids)
   
        
        
        return 'Hecho'
    except Exception as e:
        menssage=str({'error':e, 'Data':data})
        return menssage
    



    



@router.post('/tweets', response_model=Tweet, tags=["tweets"])
async def create_tweet(tweet: Tweet):
    result = conn.local.tweet.insert_one(dict(tweet))
    tweet_id = result.inserted_id 
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


