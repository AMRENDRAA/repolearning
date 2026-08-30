from fastapi import FastAPI ,UploadFile,File,HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil 

app=FastAPI()

#STEP 1 ENSURE UPLOADS FOLDER EXIST

UPLOAD_DIR="uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

#STEP2 STATIC FILE SETUP

@app.post("/upload")
def upload_file(file:UploadFile=File(...)):
    filename=file.filename
    file_path=os.path.join(UPLOAD_DIR,filename)

    if not filename:
        raise HTTPException(status_code=400 ,detail="File not selected ")
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

        return {
            "message":"File uploaded ",
            "filename":filename,
            "file_url":f"http://127.0.0.1:8000/files/{filename}"
        }

@app.get("/files/{filenames}")

def get_file(filename:str):
    file_path=os.path.join(UPLOAD_DIR,filename)

    if not os.path.exists (file_path):
        raise HTTPException(status_code=404,detail="File not found")

    return {
       "file_url":f" http://127.0.0.1:8000/files/{filename}"
    }


@app.get("/")
def home():
    return{
        "message":"File uploaded api running"
    }