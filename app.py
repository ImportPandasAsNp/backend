import os
from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn
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
    email: str | None = None
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
    # user = None
    if user is None:
        return Response(content='{"message": "user not found"}', status_code=401, media_type='application/json')

    return {"message":"user authenticated", "body":user}


@app.get("/search/text")
async def ping(q):
    print("app", q)
    res = ContentMetadataService.getIdsWithArguments({"genre": q})
    return res

@app.get("/search/voice")
async def ping():
    return {"status": 200, "value": "coming soon"}


@app.get("/recommend")
def ping():
    # print("app")
    res = ContentFeatureService.getKNNMetadataWithContentName("home alone")
    return res


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=os.getenv("PORT"))