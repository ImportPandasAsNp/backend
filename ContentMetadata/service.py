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
'''

def getIdsWithArguments(argDict):
    # print("service", argDict)
    # getIds([])
    builder = QueryBuilder.builder()

    for key in argDict.keys():
        builder.addQuery(key, argDict[key])

    if len(argDict.keys()) > 0:
        res = builder.execute()
        # print(res)
        # return res
        return getIdsFromResult(res)
    
    return {}

def getIdsFromResult(res):
    # print("service", res)
    return [data['_id'] for data in res['hits']['hits']]

if __name__=="__main__":
    print(getIdsWithArguments({
        "title":"the conjuring"
    }))

