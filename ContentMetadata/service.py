from ContentMetadata.search import getIds, QueryBuilder


def getContentMetadata(row):
    return [data for data in row['hits']['hits']]

def getMetadataWithIds(idList):
    return getContentMetadata(getIds(idList))

'''
    Arguments - 
    title - Single keyword or list of keywords
    cast - Single name or list
    director - Single name or list
    genre - Single genre or list of genre
    rating - A or U/A or U
'''

def getIdsWithArguments(argDict):
    res = getMetadataWithArguments(argDict)
    return getIdsFromResult(res)

def getMetadataWithArguments(argDict):
    builder = QueryBuilder.builder()

    for key in argDict.keys():
        if key=="rating":
            builder.addRatingQuery(argDict["rating"])
        elif key=="subscribed_platforms":
            builder.addPlatformsQuery(argDict["subscribed_platforms"])
        else:
            builder.addQuery(key, argDict[key])


    if len(argDict.keys()) > 0:
        res = builder.execute()
        return res['hits']['hits']
    
    return {}

def getIdsFromResult(res):
    # print("service", res)
    return [data['_id'] for data in res]

if __name__=="__main__":
    print(getIdsWithArguments({
        "title":"the conjuring"
    }))

