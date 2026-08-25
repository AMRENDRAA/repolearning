from fastapi import FastAPI
app=FastAPI()
#Home Route 

@app.get("/")
def new():
    return {"Jai shree ram "}


#about route
@app.get("/about")
def about():
    return {"message":"This is about route"}

#user route

@app.get("/users")
def user_get():
    return {"message":"This is users router"}


