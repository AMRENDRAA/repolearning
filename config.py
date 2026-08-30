import os
from dotenv import load_dotenv 

load_dotenv()

class Settings:
    origins = os.getenv("ORIGINS")
    SECRET_KEY = os.getenv("SECRET_KEY")
    db_url = os.getenv("DB_URL")

# FIX: Change 'setting = Settings' to plural and add parentheses ()
settings = Settings()
