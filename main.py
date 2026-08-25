from fastapi import FastAPI
app=FastAPI()

#Path parameter
@app.get("/users/{user_id}")
def get_userid(user_id :int ):
    return {"id":user_id}
