from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()




class User (BaseModel):
    name:str
    rollno:int
    Address:address

class address(BaseModel):
    city:str
    pincode:int


@app.post("/create_post")
def create_user(suer:User):
    return{
        "message":"Hello created user",
        "Data":suer
    }







