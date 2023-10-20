import os
import openai
import requests
from fastapi import FastAPI, Response, Request, Header
from pydantic import BaseModel
from typing import List
import uvicorn
import json
from dotenv import load_dotenv

from es import esclient
from ContentMetadata import service as ContentMetadataService
from ContentFeatures import service as ContentFeatureService
from UserMetadata import service as UserMetadataService
from UserHistory import service as UserHistoryService


from Recommendation.reranking import getFinalRecommendationsWithId, getFinalRecommendationsWithName
from Recommendation.filtered import *

load_dotenv()
app = FastAPI()
esclient.getClient()
# print(es.ping)
openai.api_key=os.getenv("open_ai_api_key")

@app.get("/")
async def ping(authorization: str = Header(None)):
    token = authorization.split(' ')[1]
    print("app, /", authorization, token)
    return {"message":"Server is Live"}

class Auth(BaseModel):
    name: str
    email: str
    password: str

class WatchHistory(BaseModel):
    movie_id: str
    # start_time: float
    duration: int
    # rating: float

class UserProfile(BaseModel):
    name: str
    age_filter: str
    country: str    
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
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    res = UserMetadataService.updateProfile(token, { "name": req.name, "age_filter": req.age_filter, "country": req.country, "genre": req.genre })
    return res

@app.get("/history")
async def ping(authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    res = UserHistoryService.getHistoryFromId(user_id)
    return res

@app.put("/history")
async def ping(req: WatchHistory, authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    res = UserHistoryService.updateUserHistory(user_id, [ req.movie_id, req.duration ])
    return res


@app.get("/search")
async def ping(query: str) -> []:
    req = [
        {
            "content": "You are a keyword extractor. Extract the director, cast, genre and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown",
            "role": "system"
        },
        {
            "content": query,
            "role": "user"
        }
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= req
    )

    parsed_text = completion.choices[0].message.content
    print("qq", parsed_text)
    # parsed_text="Title: None Provided\nDirector: Christopher Nolan\nCast: Tom Hardy\nGenre: None Provided"
    parsed_fields = parsed_text.lower().split("\n")
    req = dict()
    for item in parsed_fields:
        tmp=item.split(":")
        val = tmp[1].strip().split(", ")
        if len(val) == 1:
            if val[0] != "unknown":
                req.setdefault(tmp[0].strip(), val[0])
            continue
        
        req.setdefault(tmp[0].strip(), val)
            
    
    print(req)

    res = filterQuery('123456',req)
    return res


@app.post("/recommend")
async def ping(request: Request):
    request =  await request.body()
    request = json.loads(request.decode())
    userId = request["id"]
    queryDict = None
    
    if 'query' in request:
        queryDict = request['query']

    res = getFinalRecommendationsWithName(userId, queryDict)
    return res

# @app.post("/recommend")
# async def ping(query: Request, authorization: str = Header(None)):
#     # if not authorization:
#     #     return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
#     # token = authorization.split(' ')[1]
#     token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
#     user_id = UserMetadataService.getUserIdFromToken(token)

#     request =  await query.body()
#     request = json.loads(request.decode())
    
#     return getFinalRecommendationsWithId(user_id, queryDict=request)


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=os.getenv("PORT"))