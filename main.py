from fastapi import FastAPI ,Depends,Header,HTTPException
app=FastAPI()


# def common_function():
#     print("this is common function will be used as dependency injection")


# @app.get("/depends")
# def dependf(data=Depends(common_function)):
#     return data


# @app.get("/injection")
# def get_current_user(data=Depends(common_function)):
#     return {
#         data
#     }


def verify_token(token:str=Header(None)):
    if token!="mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail="unauthorized"
        )
    return {
        "user":"Authorized "
    }


@app.get("/secure")
def check_secure(user=Depends(verify_token)):
    return{
        "message":"Secure",
        "data":user
    }