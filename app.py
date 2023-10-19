import os
import time
from fastapi import FastAPI, Response, Request, Header
from pydantic import BaseModel
from typing import List
import uvicorn
import json
from dotenv import load_dotenv
# from models import Content
# import models

from es import esclient
from ContentMetadata import service as ContentMetadataService
from ContentFeatures import service as ContentFeatureService
from UserMetadata import service as UserMetadataService

load_dotenv()
app = FastAPI()
esclient.getClient()
# print(es.ping)

@app.get("/")
async def ping(authorization: str = Header(None)):
    token = authorization.split(' ')[1]
    print("app, /", authorization, token)
    return {"message":"Server is Live"}

class Auth(BaseModel):
    name: str | None = None
    email: str
    password: str

class WatchHistory(BaseModel):
    movie_id: str
    start_time: float
    duration: int
    rating: float

class UserProfile(BaseModel):
    name: str | None = None
    age_filter: str | None = None
    country: str | None = None    
    genre: List[str]

@app.post("/auth/signup")
async def ping(req: Auth):
    res = UserMetadataService.createUser(req.name, req.email, req.password)
    return res

@app.post("/auth/signin")
async def ping(req: Auth):
    res = UserMetadataService.chkUser(req.email, req.password)
    return res

@app.put("/profile")
async def ping(req: UserProfile, authorization: str = Header(None)):
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    res = UserMetadataService.updateProfile(token, { "name": req.name, "age_filter": req.age_filter, "country": req.country, "genre": req.genre })
    return res


@app.get("/search/text")
async def ping(request: str) -> []:
    # print("app", q)
    # request =  await request.body()
    # request = json.loads(request.decode())

    # if 'query' not in request.keys():
    #     return []
    
    # res = ContentMetadataService.getMetadataWithArguments(request["query"])

    res = ContentMetadataService.getMetadataWithArguments({"genre": request})
    return res

@app.get("/search/voice")
async def ping():
    return {"status": 200, "value": "coming soon"}


@app.post("/recommend")
async def ping(request: Request):
    request =  await request.body()
    request = json.loads(request.decode())
    movieName = request["name"]
    queryDict = None
    
    if 'query' in request:
        queryDict = request['query']

    res = ContentFeatureService.getKNNMetadataWithContentName(movieName, queryDict)
    return res


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=os.getenv("PORT"))