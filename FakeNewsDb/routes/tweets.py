from fastapi import APIRouter, HTTPException, status, Response
from models.tweet import Tweet
from config.db import conn
from config.twitter import client, api
from config.openai import openai
from schemas.tweet import serializeDict, tweetsEntity, serializeList, tweetEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

import pandas as pd
import json
import requests
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
   #git flow despliegue con jenkeys para liberty
        
        
        return 'Hecho'
    except Exception as e:
        menssage=str({'error':e, 'Data':data})
        return menssage
 
@router.post('/tweets', response_model=Tweet, tags=["tweets"])
async def create_tweet(tweet: Tweet):
    result = conn.local.tweet.insert_one(dict(tweet))
    tweet_id = result.inserted_id 
    return serializeDict(conn.local.tweet.find_one({"_id":tweet_id}))

#metodos de notificaciones para las noticias metodos manueles con la api 
@router.post('/send_sms_manual/{numero}', tags=["tweets"])
async def create_tweet(phone_number: str, message: str):
    url = 'https://2myuqf82ki.execute-api.us-east-1.amazonaws.com/default/sms'
    data = {
        'phone_number': phone_number,
        'answer': message
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="SMS sending failed")

    return {"status_code": response.status_code, "response": response.text}
    
    
#Metodo de notificación por medio de la api de gmail, metodo manual
@router.post('/send_mail_manual/{numero}', tags=["tweets"])
async def create_tweet(phone_number: str, message: str):
    url = 'https://2myuqf82ki.execute-api.us-east-1.amazonaws.com/default/sms'
    data = {
        'phone_number': phone_number,
        'answer': message
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="SMS sending failed")

    return {"status_code": response.status_code, "response": response.text}


     


@router.put("/tweets/{id}", response_model=Tweet, tags=["tweets"])
async def update_tweet(id: str, tweet: Tweet):
    conn.local.tweet.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(tweet)
    })
    return serializeDict(conn.local.tweet.find_one({"_id":ObjectId(id)}))

@router.put("/tweets/{id}/veracidad",response_model=Tweet, tags=["tweets"])
async def update_tweet_veracidad(id: str, veracidad: str):
    response = conn.local.tweet.find_one_and_update({"_id":ObjectId(id)},{
        "$set":{"verasidad": veracidad}
    })
    response = conn.local.tweet.find_one({"_id":ObjectId(id)})
    return serializeDict(response)


@router.delete("/tweets/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tweets"])
async def delete_tweet(id: str):
     conn.local.tweet.find_one_and_delete({
        "_id": ObjectId(id)
    })
     return Response(status_code=HTTP_204_NO_CONTENT)


@router.post("/verificar_noticia_openai/{noticia}",tags=["tweets"])
async def verificar_noticia(noticia: str):

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Eres un sistema de verficacion de informacion, lees una nota y determinas aproximadamente si la informacion es verdad o falsa, si es verdad respondes V y si es falsa F"
            },
            {
            "role": "user",
            "content": "Noticia: @petrogustavo pagándole a delincuentes de nuestro bolsillo,  Mejor le hubiera bajado al gasto públicos de congresistas , concejales , diputados "
            },
            {
            "role": "assistant",
            "content": "F | p=0.95"
            },
            {
                "role": "user",
                "content": noticia
            }
        ],
        temperature=1,
        max_tokens=10,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return {"respuesta": response.choices[0].message['content']}
