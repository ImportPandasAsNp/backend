from ContentFeatures.service import getKNNMetadataWithFeature
from UserFeatures.service import getFeaturesWithId
from Recommendation.reranking import reranking
from UserHistory.service import getHistoryFromId
from ContentMetadata.service import getMetadataWithIds,getMetadataWithArguments

#filter on user preferences and rerank
def filterQuery(userId, queryDict):
    userFeatures = getFeaturesWithId(userId)
    movieData = getKNNMetadataWithFeature(userFeatures,queryDict,returnFeatures=True)
    movieData = reranking(userFeatures,movieData)

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
        'rating':queryDict['rating']
    })

    return {"key":maxKey,"data":filteredMetadata}