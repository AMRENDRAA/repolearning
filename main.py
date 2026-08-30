from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv 

app=FastAPI()
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

@app.get("/")
def home():
    return {
        "message":SECRET_KEY
    }