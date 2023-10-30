from ContentFeatures.service import getKNNMetadataWithFeature
from UserFeatures.service import getFeaturesWithId
from Recommendation.reranking import reranking
from UserHistory.service import getHistoryFromId
from ContentMetadata.service import getMetadataWithIds,getMetadataWithArguments
from UserSubscriptions.service import getSubscriptionsFromId
from Utils.constants import PLATFORMS
import random
from SessionContext.mem_db import userSessionVectorClient


def averageVectors(vectorList):
    if not vectorList:
        return []

    # Ensure all vectors are of the same length
    vectorLength = len(vectorList[0])
    if not all(len(vector) == vectorLength for vector in vectorList):
        raise ValueError("All input vectors must have the same length")

    # Initialize the sum of vectors
    sumVector = [0] * vectorLength

    # Calculate the sum of vectors
    for vector in vectorList:
        sumVector = [sum(x) for x in zip(sumVector, vector)]

    # Calculate the average vector
    averageVector = [x / len(vectorList) for x in sumVector]

    return averageVector


#filter on user preferences and rerank
def filterQuery(userId, queryDict):
    userFeatures = getFeaturesWithId(userId)

    if len(userFeatures)==0:
        movieData = getMetadataWithArguments(queryDict)
        return random.sample(movieData,min(len(movieData),20))
    
    movieData = getKNNMetadataWithFeature(userFeatures,queryDict,returnFeatures=True)
    movieData = reranking(userFeatures,movieData)

    avg = []

    for i in range(0,min(3,len(movieData))):
        avg.append(movieData[i]['feature'])

    avg = averageVectors(avg)
    userSessionVectorClient.addVector(id,avg)

    for data in movieData:
        del data['feature']

    return movieData

def filterQueryWithFeatures(userId,feat,queryDict):
    userFeatures = getFeaturesWithId(userId)
    movieData = getKNNMetadataWithFeature(feat,queryDict,returnFeatures=True)

    if len(userFeatures)>0:
        movieData = reranking(userFeatures,movieData)

    else:
        movieData = reranking(feat, movieData)
    avg = []

    for i in range(0,min(3,len(movieData))):
        avg.append(movieData[i]['feature'])

    avg = averageVectors(avg)
    userSessionVectorClient.addVector(id,avg)
    
    for data in movieData:
        del data['feature']

    return movieData

def getMostFrequent(id, key,queryDict=None):
    history = getHistoryFromId(id)
    userFeature = getFeaturesWithId(id)

    if len(history)==0:
        return []
    
    print(history)
    movieIds = []

    for his in range((max(0,len(history)-10)),len(history)):
        element = history[his]
        movieIds.append(element[0])

    # movieIds = list(set(movieIds))
    cntid = dict()

    for id in movieIds:
        if id not in cntid:
            cntid[id]=1
        else:
            cntid[id]+=1

    contentMetadata = getMetadataWithIds(movieIds)

    keyDict = dict()

    for metadata in contentMetadata:
        splitted = metadata["_source"][key].split(',')

        if splitted[0] not in keyDict:
            keyDict[splitted[0]]=cntid[metadata["_id"]]
        else:
            keyDict[splitted[0]]+=cntid[metadata["_id"]]
        # for dir in splitted:
        #     if dir not in keyDict:
        #         keyDict[dir]=1
        #     else:
        #         keyDict[dir]+=1

    print(keyDict)
    
    maxKey = max(zip(keyDict.values(), keyDict.keys()))[1]

    filteredMetadata = getKNNMetadataWithFeature(userFeature,{
        key:maxKey,
        'rating':queryDict['rating'],
        "subscribed_platforms":queryDict["subscribed_platforms"]
    })

    return {"key":maxKey,"data":filteredMetadata}


def recommendOtherPlatforms(id, queryDict=None):
    subs = getSubscriptionsFromId(id)
    if queryDict is None:
        queryDict = dict()

    if "rating" not in queryDict:
        queryDict["rating"]="A"

    userFeatures = getFeaturesWithId(id)
    otherPlatforms = [p for p in PLATFORMS if p not in subs]
    movieData = []

    if len(otherPlatforms)==0:
        return [],"None"

    if len(userFeatures)==0 and "genre" in queryDict:
        print("Here")
        for p in otherPlatforms:
            movieData.extend(getMetadataWithArguments({
                "genre":queryDict["genre"],
                "platform":p,
                "rating":queryDict["rating"]
            }))

        return random.sample(movieData,min(len(movieData),20)),otherPlatforms[0]

    else:
        del queryDict['genre']

    
    for p in otherPlatforms:
        movieData.extend(getKNNMetadataWithFeature(userFeatures,{
            "platform":p,
            "rating":queryDict["rating"]
        },returnFeatures=True))

    movieData = reranking(userFeatures,movieData,returnDot=True)

    for data in movieData:
        del data['feature']

    movieData = movieData[0:min(len(movieData),20)]
    
    dotDict = dict()

    for data in movieData:
        print(data)
        if data['_source']['platform'] not in dotDict:
            dotDict[data['_source']['platform']] = list()
            dotDict[data['_source']['platform']].append(data['dot'])
        
        else:
            dotDict[data['_source']['platform']].append(data['dot'])

    for key in dotDict:
        dotDict[key] = sum(dotDict[key])/len(dotDict[key])
    maxKey = max(dotDict,key=dotDict.get)

    return movieData,maxKey




