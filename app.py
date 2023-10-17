import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
# from models import Content
# import models

from es import ESclient

load_dotenv()
app = FastAPI()
esclient = ESclient()
es = esclient.getClient()
esclient.getClient()
# print(es.ping)

@app.get("/")
async def ping():
    return "Server is Live and Running"

@app.get("/search/text")
async def ping(q):
    return q

@app.get("/search/voice")
async def ping():
    return {"status": 200, "value": "coming soon"}




if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=os.getenv("PORT"))