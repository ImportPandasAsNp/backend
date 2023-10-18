import os
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
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
async def ping():
    return {"message":"Server is Live"}

class Auth(BaseModel):
    email: str
    user_name: str
    password: str

@app.post("/auth/signup")
async def ping():
    print("app")
    # res = ContentMetadataService.getIdsWithArguments({"genre": q})
    return

@app.post("/auth/signin")
async def ping(req: Auth):
    print("app", req)
    user = UserMetadataService.chk_user(req.user_name, req.password)
    # user = Noney
    if user is None:
        return Response(content='{"message": "user not found"}', status_code=401, media_type='application/json')

    return {"message":"user authenticated", "body":user}


@app.post("/search/text")
async def ping(request: Request):
    # print("app", q)
    request =  await request.body()
    request = json.loads(request.decode())

    if 'query' not in request.keys():
        return []
    
    res = ContentMetadataService.getIdsWithArguments(request["query"])
    movies = ContentMetadataService.getMetadataWithIds(res)
    return movies

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