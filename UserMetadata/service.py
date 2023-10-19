import os
from UserMetadata.search import getIds, QueryBuilder
from passlib.context import CryptContext
from Utils import api
from jose import jwt
from fastapi import Response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def getUserMetadata(row):
    return [data for data in row['hits']['hits']]

def getMetadataWithIds(idList):
    return getUserMetadata(getIds(idList))

def getIdsWithArguments(argDict):
    res = getIdsWithArguments(argDict)
    return getIdsFromResult(res)

def getMetadataWithArguments(argDict):
    builder = QueryBuilder.builder()

    for key in argDict.keys():
        builder.addQuery(key, argDict[key])

    if len(argDict.keys()) > 0:
        res = builder.execute()
        return res['hits']['hits']
    
    return {}

def getIdsFromResult(res):
    return [data['_id'] for data in res['hits']['hits']]

def chkUser(email: str, password: str) -> dict:
    user = getMetadataWithArguments({"email": email})
    print("service", user)
    if not user:
        return Response(content='{"message": "user not registered"}', status_code=401, media_type='application/json')
    if not verify_password(password, user[0]["_source"]["password"]):
        return Response(content='{"message": "Invalid credntials"}', status_code=401, media_type='application/json')
    
    token = jwt.encode({"user_id": user[0]["_id"]}, os.getenv("jwt_secret"))
    # print("chkUser", getUserIdFromToken(token))
    return {"message":"user authenticated", "body":{"user": user[0]["_source"], "token": token}}

def createUser(name: str, email: str, password: str) -> dict:
    user = getMetadataWithArguments({"email": email})
    if user:
        return Response(content='{"message": "user already exists"}', status_code=401, media_type='application/json')
    hashed_password = get_password_hash(password)
    res = api.insertRecord("user_metadata", {"name":name, "email":email, "password":hashed_password, "country":"United States", "age_filter":"R", "genre":"comedy"})    
    print("service", res)
    if res["result"] != "created":
        return Response(content='{"message": "Internal server error"}', status_code=500, media_type='application/json')
    
    token = jwt.encode({"user_id": res["_id"]}, os.getenv("jwt_secret"))
    
    return {"message":"user authenticated", "body":{"user": user, "token": token}}

def getUserIdFromToken(token):
    res = jwt.decode(token, os.getenv("jwt_secret"))
    return res["user_id"]

def updateProfile(token, req):
    user_id = getUserIdFromToken(token)
    res = api.updateRecord("user_metadata", user_id, req)
    return req


if __name__=="__main__":
    print(getIdsWithArguments({
        "title":"the conjuring"
    }))

