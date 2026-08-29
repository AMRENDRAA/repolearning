# 1. IMPORT NECESSARY MODULES
# create_engine: Core bridge to database; Column/Integer/String: Schema definition tools
from sqlalchemy import create_engine, Column, Integer, String 
# declarative_base: Base class for models; sessionmaker: Factory for DB sessions; Session: Type hint
from sqlalchemy.orm import declarative_base, sessionmaker, Session
# FastAPI: Web framework instance; Depends: Dependency injection manager for clean resource handling
from fastapi import FastAPI, Depends,HTTPException
# BaseModel: Used to define structural rules for incoming JSON request bodies
from pydantic import BaseModel

# 2. APPLICATION INITIALISATION
# Create the central FastAPI application instance to route web traffic
app = FastAPI()

# 3. DATABASE CONFIGURATION
# Define connection string; 'sqlite:///' creates a local file database called 'test.db' in this folder
DATABASE_URL = "sqlite:///./test.db"

# 4. ENGINE CREATION
# The engine acts as the underlying hub connecting Python code to the database file
# 'check_same_thread=False' allows multiple asynchronous FastAPI requests to access SQLite safely
engine = create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False
})

# 5. SESSION FACTORY
# SessionLocal is a class factory configured to spin up fresh database transaction blocks
# 'autocommit=False' ensures changes must be explicitly saved; 'autoflush=False' holds sync until query execution
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. ORM BASE CLASS
# Construct the core Base class; all database tables must inherit from this to map to the engine
Base = declarative_base()

# 7. DATABASE MODEL (TABLE) DEFINITION
# This Python class translates directly into an actual structural table in the database
class Todo(Base):
    __tablename__ = "todos"  # Sets the physical name of the table inside SQLite

    # Primary key column; 'index=True' makes searches via ID incredibly fast; auto-increments by default
    id = Column(Integer, primary_key=True, index=True)
    # Simple text columns to hold individual todo descriptions and their statuses
    title = Column(String)
    completed = Column(String)

# 8. PHYSICAL TABLE INITIALISATION
# Looks at all models inheriting from 'Base' and physically builds the tables in the file if missing
Base.metadata.create_all(bind=engine)

# 9. DATABASE LIFECYCLE DEPENDENCY (MANAGEMENT)
# This function handles opening and securely closing database connections per request
def get_db():
    db = SessionLocal()  # Instantiate a unique transaction session
    try:
        yield db         # Provide the active connection stream to the requesting API endpoint
    finally:
        db.close()       # Safely shut down the connection when the API request completely finishes

# 10. REQUEST BODY SCHEMA
# This Pydantic model forces FastAPI to look for 'title' inside the incoming JSON payload
class TodoCreate(BaseModel):
    title: str

# 11. API ENDPOINT ROUTE
@app.post("/todos")
# By using 'todo_in: TodoCreate', FastAPI automatically parses the JSON body
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    # Dig out the string description using dot notation (.title)
    todo = Todo(title=todo_in.title, completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        "message": "Todo created",
        "data": todo
    }


@app.get("/todos")


def get_todos(db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    return {
        "total":len(todos),
        "data":todos
    }


@app.get("/todos/{todo_id}")
def get_todo(todo_id:int ,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404 ,detail="Todo not found")

    return {
        todo
    }


@app.put("/todos/{todo_id}")
def update_todo(todo_id:int ,title:str ,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = title

    db.commit()
    db.refresh(todo)

    return{
        "message":"Todo update",
        "data":todo

    }


#delete 

@app.delete("/todos/{todo_id}")

def delete_todo(todo_id:int ,db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {
        "message":"delted "
    }



