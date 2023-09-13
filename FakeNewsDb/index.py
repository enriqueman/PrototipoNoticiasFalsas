from fastapi import FastAPI
from routes.user import user
from routes.tweets import router
from routes.news import news
from routes.usertweets import usertweet


app = FastAPI(

    title="FastAPI & Mongo CRUD",
    description="this is a simple REST API using fastapi and mongodb",
    version="0.0.1",
   
)

app.include_router(user)
app.include_router(router)
app.include_router(news)
app.include_router(usertweet)
