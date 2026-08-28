from sqlalchemy import create_engine,Column ,Integer,String 
from sqlalchemy.orm import declarative_base ,sessionmaker ,Session
from fastapi import FastAPI ,Depends


app=FastAPI()
#DB URL Pointing to a local sqlite file
DATABASE_URL="sqlite:///./test.db"

#create engine (connect args is o nly need for sqlite)

engine= create_engine(DATABASE_URL,connect_args={
    "check_same_thread":False
})

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base=declarative_base()


class Todo(Base):
    __tablename__="todos"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    completed=Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")

def home(db:Session=Depends(get_db)):
    return{
        "Message":"Db works"
    }

