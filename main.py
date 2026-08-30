from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings 

app=FastAPI()


SECRET_KEY=settings.SECRET_KEY


@app.get("/")
def home():
    return {
        "message":SECRET_KEY
    }