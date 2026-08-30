#uv pip install --system "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
from fastapi import FastAPI,HTTPException,Depends
from jose import jwt ,JWTError
from fastapi.security import OAuth2PasswordBearer ,OAuth2PasswordRequestForm 
from datetime import datetime ,timedelta ,timezone 
from passlib.context import CryptContext


app=FastAPI()
#JWT CONFIG 

SECRET_KEY="mysecret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
#Password hasing setup

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Oauthsetup

oauth2_schema=OAuth2PasswordBearer(tokenUrl="login")

#Dummy user DB 
fake_user_db={
    "admin":{
        "username":"admin",
        "hashed_password":pwd_context.hash("1234")
    }
}

#hash password 
def hash_password(password:str):
    return pwd_context.hash(password)


#verify password 
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    to_encode.update({
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token 


#Login


@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user=fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password ")
    access_token=create_token({"sub":form_data.username})
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }


def verify_token(token:str=Depends(oauth2_schema)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token "
        )



#protected route 

@app.get("/protected")
def protected_route(username:str= Depends(verify_token)):
    return {
        "message":"hello access success",
        "user":username 
    }
    






