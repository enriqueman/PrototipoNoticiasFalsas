from fastapi import APIRouter, status, Response,  UploadFile, File, HTTPException
from models.usertweets import UserTweet
from config.db import conn
from config.twitter import api
from schemas.usertweets import serializeDict, userTweetsEntity, serializeList, userTweetEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT
import pandas as pd
import json

usertweet = APIRouter()

@usertweet.get('/usertweets', response_model=list[UserTweet], tags=["UserTweets"])
async def find_all_usertweets():
    return userTweetsEntity(conn.local.usertweet.find())

@usertweet.post('/usertweets', response_model=UserTweet, tags=["UserTweets"])
async def create_usertweet(usertweet: UserTweet):
    result = conn.local.usertweet.insert_one(dict(usertweet))
    usertweet_id = result.inserted_id # obtenemos el id del documento insertado
    return serializeDict(conn.local.usertweet.find_one({"_id":usertweet_id}))

@usertweet.put("/usertweets/{id}", response_model=UserTweet, tags=["UserTweets"])
async def update_usertweet(id: str, usertweet: UserTweet):
    conn.local.usertweet.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(usertweet)
    })
    return serializeDict(conn.local.usertweet.find_one({"_id":ObjectId(id)}))

@usertweet.delete("/usertweets/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["UserTweets"])
async def delete_usertweet(id: str):
     conn.local.usertweet.find_one_and_delete({
        "_id": ObjectId(id)
    })
     return Response(status_code=HTTP_204_NO_CONTENT)



@usertweet.post('/get_user_info/{screen_name}', response_model=UserTweet ,tags=["UserTweets"])
async def save_user(screen_name: str):
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
        result = conn.local.usertweet.insert_one(response)
        usertweet_id = result.inserted_id

        menssage="entro"
    except Exception as e:
        menssage=e
        
    return userTweetEntity(conn.local.usertweet.find_one({"_id":usertweet_id}))



@usertweet.post("/read_excel/{sheet_name,column_name}", response_model=list[UserTweet],tags=["UserTweets"])
async def read_excel(sheet_name: str, column_name: str, file: UploadFile = File(...)):
    try:
        # Lee el archivo de Excel en un DataFrame de pandas
        df = pd.read_excel(file.file, sheet_name=sheet_name)

        # Verifica si la columna existe en el DataFrame
        if column_name not in df.columns:
            raise HTTPException(status_code=400, detail=f"La columna '{column_name}' no existe en la hoja '{sheet_name}'")

        # Devuelve los datos de la columna especificada
        
        screen_names= df[column_name].tolist()

        for screen_name in screen_names:
            try:
                user = api.get_user(screen_name=screen_name)
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
                result = conn.local.usertweet.insert_one(response)
                
                menssage="entro"
            except Exception as e:
                menssage=e
        
           



        return userTweetsEntity(conn.local.usertweet.find())
    #df[column_name].tolist()
    

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))