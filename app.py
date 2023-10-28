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

from Utils.helpers import *

from ContentMetadata import service as ContentMetadataService
from ContentFeatures import service as ContentFeatureService
from UserMetadata import service as UserMetadataService
from UserHistory import service as UserHistoryService
from UserSubscriptions import service as UserSubscriptionsService

from UserChatContext.mem_db import userChatClient

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
userChatClient.getClient()
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
    # print(request)
    # print(recommendOtherPlatforms(user_id, request))
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
    print("Subscriptions ",userSubscriptions)

    # if len(userSubscriptions)==0:
    #     return []
    prompt_req = [
        {
            "content": "You are an intelligent keyword extractor. Extract the director, cast, genre, plot and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown. When u see the phrase 'show me a movie by', assume it means the actor, directed by will be specified separately for directors. Return in the following format { 'title': '',	'director': [],	'genre': [], 'cast': [], 'plot': '' } \ntitle: will be the title of the movie\ndirector: will be the list of the directors\ncast: will be the list of cast members\ngenre: will be the list of genres from the following list ['parody', 'cult', 'spyespionage', 'buddy', 'romance', 'music', 'historical', 'anthology', 'faith and spirituality', 'action', 'teen tv shows', 'tv shows', 'docuseries', 'animation', 'series', 'drama', 'adventure', 'documentary', 'medical', 'international', 'game show competition', 'reality', 'anime', 'horror', 'travel', 'talk show and variety', 'superhero', 'arts', 'talk show', 'entertainment', 'arthouse', 'young adult audience', 'spanish', 'sports', 'movies', 'scifi', 'british', 'mystery', 'biographical', 'korean', 'culture', 'romantic comedy', 'unscripted', 'coming of age', 'science nature', 'dance', 'policecop', 'fitness', 'comedy', 'suspense', 'scifi fantasy', 'science fiction', 'classic movies', 'kids', 'animals  nature', 'lifestyle', 'disaster', 'independent', 'soap opera melodrama', 'western', 'documentaries', 'family', 'fantasy', 'variety', 'survival', 'action adventure', 'concert film', 'thriller', 'lgbtq', 'special interest', 'crime', 'military and war'].\nplot: this is a string field, try to find any segments of the query that is relevant to plot information. Replace proper nouns with templates like man/woman depending on their gender.\nFor every field mentioned above there is no compulsion to fill it. If not found mention unknown for title or plot or return empty list for genre, cast or director. Often you will be provided with text which will not contain multiple fields mentioned above, you are not compelled to fill them.\n",
            "role": "system"
        },
        {
            "content": query,
            "role": "user"
        }
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt_req
    )

    parsed_dict = completion.choices[0].message.content
    print("qq", parsed_dict)

    req_dict = userChatClient.addContext(user_id, parsed_dict)
    req = getQuery(req_dict)
    print(req)

    req['rating'] = request['rating']
    req["subscribed_platforms"] = userSubscriptions
    print(req)

    if len(req.keys())==2:
        queryFeat = ModelEmbeddings.getEmbeddings(query)
        return filterQueryWithFeatures(user_id,queryFeat,req)

    res = filterQuery(user_id, req)
    return res

@app.get("/search/clear")
async def ping(authorization: str = Header(None)) -> []:
    if not authorization:
        return Response(content='{"message": "user not authenticated"}', status_code=403, media_type='application/json')
    token = authorization.split(' ')[1]

    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTHY2YVJvc0JHWkJrWnJhVmJ5bGEifQ.zFGj-07jTAwF74fI0Fqcs6B1RJOyvaBdGKrVyTFiyn8"
    user_id = UserMetadataService.getUserIdFromToken(token)
    try: 
        userChatClient.removeContext(user_id)
        return Response(content='{"message": "user chat context removed"}', status_code=200, media_type='application/json')
    except:
        return Response(content='{"message": "user chat context not removed"}', status_code=500, media_type='application/json')
        

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
