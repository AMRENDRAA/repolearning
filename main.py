# 1. IMPORT NECESSARY MODULES
# create_engine: Core bridge to database; Column/Integer/String: Schema definition tools
from sqlalchemy import create_engine, Column, Integer, String 
# declarative_base: Base class for models; sessionmaker: Factory for DB sessions; Session: Type hint
from sqlalchemy.orm import declarative_base, sessionmaker, Session
# FastAPI: Web framework instance; Depends: Dependency injection manager for clean resource handling
from fastapi import FastAPI, Depends

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

# 10. API ENDPOINT ROUTE
# Decorator capturing basic web GET requests hitting the home path '/'
@app.get("/")
def home(db: Session = Depends(get_db)): # Injects a temporary database session securely into the local variable 'db'
    return {
        "Message": "Db works"  # Basic JSON proof-of-concept payload returned to client
    }
