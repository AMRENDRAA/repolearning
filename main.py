from fastapi import FastAPI, Depends ,HTTPException 
from sqlalchemy.orm import Session 
from database import engine,SessionLocal
import model,schemas 

from auth import create_token ,verify_token 
from fastapi import BackgroundTasks
from email_utils import send_email
import os
MY_TEST_EMAIL = os.getenv("TEST_EMAIL")

#db dependency

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()



model.Base.metadata.create_all(bind=engine)
app=FastAPI()
@app.get("/")
def home():
    return {
        "message":" Jai shree Ram Blog api"
    }


#login api
@app.post("/login")
def login():
    return{
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"

    }

#create blog



@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,background_tasks: BackgroundTasks,db:Session=Depends(get_db),user=Depends(verify_token )):
    new_blog=model.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    background_tasks.add_task(
        send_email,
        to_email=MY_TEST_EMAIL,
        subject="Your blog was created!",
        body=f"Hi, your blog '{new_blog.title}' was created successfully."
    )
   
    

    return new_blog 




@app.get("/blogs",response_model=list[schemas.BlogResponse])
def get_blogs(db: Session =Depends(get_db)):
    return db.query(model.Blog).all()



@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_blog(id:int ,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=404,detail="Not foudn")
    return blog



@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int ,blog:schemas.BlogCreate,db: Session =Depends(get_db)):
    existing_blog= db.query(model.Blog).filter(model.Blog.id==id).first()

    if not existing_blog:
        raise HTTPException(status_code=404,detail="Not found")
    existing_blog.title=blog.title
    existing_blog.content=blog.content

    db.commit(
    )
    return existing_blog



@app.delete("/blogs/{id}")

def delete_blog(id:int ,db:Session=Depends(get_db)):
    ans=db.query(model.Blog).filter(model.Blog.id==id).first()
    if not ans:
        raise HTTPException(status_code=404,detail="Not found")
    db.delete(ans)
    db.commit()
    return {"message":"Blog deleted"}





    
    



