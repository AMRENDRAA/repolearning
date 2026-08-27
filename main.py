from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
app=FastAPI()

@app.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user():
    return {
        "message":"done "
    }

@app.get("/user")
def get_user():
    return {
        "status":"success",
        "user":"user fetched",
        "data":{
            "hello":"Jai shree ram"
        }
    }


@app.get("/user/{user_id}")
def get_user(user_id:int):
    if user_id!=1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return{
        "id":1,
        "name":"Amrendra"
    }