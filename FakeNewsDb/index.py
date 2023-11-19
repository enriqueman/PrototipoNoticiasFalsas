from fastapi import FastAPI
from routes.user import user
from routes.tweets import router
from routes.news import news
from routes.usertweets import usertweet
from routes.notificaciones import notificaciones

app = FastAPI(
    
    title="Sistema de Alerta Temprana para Notificación de Noticias Falsas",
    description="Sistema de alerta temprana construido para notificar de manera oportuna potenciales tweets que pueden carecer de veracidad",
    version="0.0.1",
   
)

app.include_router(user)
app.include_router(router)
app.include_router(news)
app.include_router(usertweet)
app.include_router(notificaciones)
