import os
import openai
import requests
from fastapi import FastAPI, Response, Request, Header
from fastapi.middleware.cors import CORSMiddleware
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
from UserSubscriptions import service as UserSubscriptionsService


from Recommendation.reranking import getFinalRecommendationsWithId, getFinalRecommendationsWithName
from Recommendation.filtered import *

from modelfeatures import ModelEmbeddings


load_dotenv()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

esclient.getClient()
# print(es.ping)
openai.api_key = os.getenv("open_ai_api_key")


@app.get("/")
async def ping(authorization: str = Header(None)):
    token = authorization.split(' ')[1]
    print("app, /", authorization, token)
    return {"message": "Server is Live"}


class Auth(BaseModel):
    name: str
    email: str
    password: str
    genre: str


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
    print(req)
    res = UserMetadataService.createUser(req.name, req.email, req.password,req.genre)
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
    res = UserMetadataService.updateProfile(
        token, {"name": req.name, "age_filter": req.age_filter, "country": req.country, "genre": req.genre})
    return res


@app.get("/history")
async def ping(authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    res = UserHistoryService.getContentMetadataHistoryFromId(user_id)
    return res


@app.put("/history")
async def ping(req: WatchHistory, authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    res = UserHistoryService.updateUserHistory(
        user_id, [req.movie_id, req.duration])
    return res

@app.put("/subscriptions")
async def ping(req: Request, authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]

    request = await req.body()
    request = json.loads(request.decode())
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    res = UserSubscriptionsService.updateUserSubscriptions(user_id,request["platform"])
    return res


@app.post("/recommend/mostfrequent/{key}")
async def ping(key, request:Request,authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')


    token = authorization.split(' ')[1]
    request = await request.body()
    request = json.loads(request.decode())
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    userSubscriptions = UserSubscriptionsService.getSubscriptionsFromId(user_id)

    if len(userSubscriptions)==0:
        return []
    
    request["subscribed_platforms"] = userSubscriptions
    print(request)
    return getMostFrequent(user_id, key,request)


@app.post("/recommend")
async def ping(query: Request,authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]

    #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    userSubscriptions = UserSubscriptionsService.getSubscriptionsFromId(user_id)

    if len(userSubscriptions)==0:
        return []

    userMetadata = UserMetadataService.getMetadataWithIds([user_id])

    request = await query.body()
    request = json.loads(request.decode())

    if request is None:
        request = dict()

    request['genre'] = userMetadata[0]["_source"]["genre"]
    request["subscribed_platforms"] = userSubscriptions
    
    # return userMetadata
    print(request)
    return getFinalRecommendationsWithId(user_id, queryDict=request)

@app.post("/recommend/otherplatforms")
async def ping(query: Request,authorization: str = Header(None)):
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]
    #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)

    userMetadata = UserMetadataService.getMetadataWithIds([user_id])

    request = await query.body()
    request = json.loads(request.decode())

    if request is None:
        request = dict()

    request['genre'] = userMetadata[0]["_source"]["genre"]
    
    # return userMetadata
    print(request)
    return recommendOtherPlatforms(user_id, request)


@app.post("/search")
async def ping(query: str,request:Request, authorization: str = Header(None)) -> []:
    print(query)
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]

    request = await request.body()
    request = json.loads(request.decode())


    #token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)

    userSubscriptions = UserSubscriptionsService.getSubscriptionsFromId(user_id)

    if len(userSubscriptions)==0:
        return []
    req = [
        {
            "content": "You are a keyword extractor. Extract the director, cast, genre and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown. When u see the phrase 'show me a movie by', assume it means the actor, directed by will be specified separately. Try to classify query into genres 'parody', 'cult', 'spyespionage', 'buddy', 'romance', 'music', 'historical', 'anthology', 'faith and spirituality', 'action', 'teen tv shows', 'tv shows', 'docuseries', 'animation', 'series', 'drama', 'adventure', 'documentary', 'medical', 'international', 'game show competition', 'reality', 'anime', 'horror', 'travel', 'talk show and variety', 'superhero', 'arts', 'talk show', 'entertainment', 'arthouse', 'young adult audience', 'spanish', 'sports', 'movies', 'scifi', 'british', 'mystery', 'biographical', 'korean', 'culture', 'romantic comedy', 'unscripted', 'coming of age', 'science nature', 'dance', 'policecop', 'fitness', 'comedy', 'suspense', 'scifi fantasy', 'science fiction', 'classic movies', 'kids', 'animals  nature', 'lifestyle', 'disaster', 'independent', 'soap opera melodrama', 'western', 'documentaries', 'family', 'fantasy', 'variety', 'survival', 'action adventure', 'concert film', 'thriller', 'lgbtq', 'special interest', 'crime', 'military and war' however this is no compulsion and classify into unknown if not possible. Genre should only be the keywords provided or unknown. Output only a single genre type for each query. Format will be Title: <title>\nDirector: <director>\nCast: <list of cast members>\nGenre: <genre>",
            "role": "system"
        },
        {
            "content": query,
            "role": "user"
        }
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=req
    )

    parsed_text = completion.choices[0].message.content
    print(parsed_text)
    print("qq", parsed_text)
    # parsed_text="Title: None Provided\nDirector: Christopher Nolan\nCast: Tom Hardy\nGenre: None Provided"
    parsed_fields = parsed_text.lower().split("\n")
    req = dict()
    for item in parsed_fields:
        tmp = item.split(":")
        val = tmp[1].strip().split(", ")
        if len(val) == 1:
            if val[0] != "unknown":
                req.setdefault(tmp[0].strip(), val[0])
            continue

        req.setdefault(tmp[0].strip(), val)

    req['rating'] = request['rating']
    req["subscribed_platforms"] = userSubscriptions

    if len(req.keys())==2:
        queryFeat = ModelEmbeddings.getEmbeddings(query)
        return filterQueryWithFeatures(user_id,queryFeat,req)

    res = filterQuery(user_id, req)
    return res


# @app.post("/recommend")
# async def ping(request: Request):
#     request =  await request.body()
#     request = json.loads(request.decode())
#     userId = request["id"]
#     queryDict = None

#     if 'query' in request:
#         queryDict = request['query']

#     res = getFinalRecommendationsWithName(userId, queryDict)
#     return res


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=os.getenv("PORT"))
