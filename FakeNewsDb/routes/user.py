from fastapi import APIRouter, status,Response
from models.user import User 
from config.db import conn 
from schemas.user import serializeDict, usersEntity, serializeList, userEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

@user.get('/users',response_model=list[User], tags=["Users"])
async def find_all_users():
    return usersEntity(conn.local.user.find())


@user.post('/users', response_model=User, tags=["Users"])
async def create_user(user: User):
    result = conn.local.user.insert_one(dict(user))
    user_id = result.inserted_id # obtenemos el id del documento insertado
    return serializeDict(conn.local.user.find_one({"_id":user_id}))

@user.put("/users/{id}", response_model=User, tags=["Users"])
async def update_user(id: str,user: User):
    conn.local.user.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(user)
    })
    return serializeDict(conn.local.user.find_one({"_id":ObjectId(id)}))


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(id: str):
     conn.local.user.find_one_and_delete({
        "_id": ObjectId(id)
    })
     return Response(status_code=HTTP_204_NO_CONTENT)




