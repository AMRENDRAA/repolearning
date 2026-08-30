import asyncio
import time
from fastapi import FastAPI
app=FastAPI()


@app.get("/")

async def f():
    await asyncio.sleep(5)
    return {"done"}
