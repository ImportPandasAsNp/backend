from UserMetadata.search import getIds, QueryBuilder
from passlib.context import CryptContext

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
    # print("service", argDict)
    # getIds([])
    builder = QueryBuilder.builder()

    for key in argDict.keys():
        builder.addQuery(key, argDict[key])

    if len(argDict.keys()) > 0:
        res = builder.execute()
        # print(res)
        return res
        # return getIdsFromResult(res)
    
    return {}

def getIdsFromResult(res):
    # print("service", res)
    return [data['_id'] for data in res['hits']['hits']]

def chk_user(user_name: str, password: str) -> str:
    user = getIdsWithArguments({"user_name": user_name})
    if len(user) == 0:
        return None
    if not verify_password(password, user[0]["password"]):
        return None
    
    return user[0]


if __name__=="__main__":
    print(getIdsWithArguments({
        "title":"the conjuring"
    }))

