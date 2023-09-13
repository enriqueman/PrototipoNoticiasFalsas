from fastapi import APIRouter, status, Response
from models.news import News
from config.db import conn
from schemas.news import serializeDict, newsEntityList, serializeList, newsEntity
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

news = APIRouter()

@news.get('/news', response_model=list[News], tags=["news"])
async def find_all_news():
    return newsEntityList(conn.local.news.find())

@news.post('/news', response_model=News, tags=["news"])
async def create_news(news: News):
    result = conn.local.news.insert_one(dict(news))
    news_id = result.inserted_id # obtenemos el id del documento insertado
    return serializeDict(conn.local.news.find_one({"_id":news_id}))

@news.put("/news/{id}", response_model=News, tags=["news"])
async def update_news(id: str, news: News):
    conn.local.news.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(news)
    })
    return serializeDict(conn.local.news.find_one({"_id":ObjectId(id)}))

@news.delete("/news/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["news"])
async def delete_news(id: str):
     conn.local.news.find_one_and_delete({
        "_id": ObjectId(id)
    })
     return Response(status_code=HTTP_204_NO_CONTENT)
