from fastapi import FastAPI, HTTPException, Depends, Header

#IMPORT the jwt module from python -jose to handle JSON WEB TOKEN ENCODING AND DECODING 


from jose import jwt

#IMPORT DATETIME UTILITIES TO HANDLE TOKEN EXPIRATION timestamps with timezones
from datetime import datetime ,timedelta,timezone
# Initialize the FastAPI application instance
app=FastAPI()
# Define the secret key used to sign the JWT (Keep this secret and secure in production)
SECRET_KEY="MYsecret"

ALGORITHM="HS256"
# Define a helper function to generate a new JWT access token
#create token 
def create_token(data:dict):
    # Create a shallow copy of the input payload dictionary to avoid modifying the original data
    to_encode=data.copy()
     # Add the standard "exp" (expiration) claim to the payload data dictionary
    expire= datetime.now(timezone.utc)+timedelta(minutes=30)
    # Add the standard "exp" (expiration) claim to the payload data dictionary
    to_encode.update({
        "exp":expire 
    })
    # Sign and encode the payload into a JWT string using the secret key and algorithm
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token



@app.post("/login")
# Define the login route handler function accepting username and password as query parameters
def login (username :str,password:str):
    # Check if the provided credentials match the hardcoded values ("admin" and "1234")
    if username!="admin" or password!="1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or password"
        )
    # Call the helper function to generate a JWT token containing the username as the subject ("sub")

    token =create_token({
        "sub":username 
    })
    # Return the generated access token inside a JSON response body
    return {
        "accesstoken":token
    }

    #token verification

    # Define a dependency function to extract and validate the JWT token from incoming request headers

def varify_token(token: str=Header(None),alias="token"):
    try:
        # Decode and verify the token signature using the secret key and allowed algorithm
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        # Return the verified payload data (dictionary) if the token is valid
        return payload
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password or expired"
        )
#protected routed

@app.get("/secure")
# Define the endpoint function, using Depends to enforce the token verification before executing the route
def secure_data(user=Depends(varify_token)):
    return {
        "message":"Secure data accessed",
        "user":user
    }


