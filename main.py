from fastapi import FastAPI

app=FastAPI()
@app.get("/users")

def queryusers(name:str=None ):
    return {"This is query paramter ":name}


#Default parameters 
@app.get("/products")
def querydefaultparams(limit :int=10):
    return {"Limit":limit}

#Multiple parameter 
@app.get("/multiple")
def multiplequeryparameters(name:str,rollno:int ):
    return {
        "nAME":name,
        "rollno":rollno
    }