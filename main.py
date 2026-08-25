from fastapi import FastAPI

app=FastAPI()

@app.post("/create")
def create_user(user:dict):
    return{
        "message":"User created",
        "data":user
    }


