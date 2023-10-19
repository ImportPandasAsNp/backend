from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId
from ContentFeatures.service import getKNNMetadataWithFeature
from UserMetadata.service import getIdsWithArguments as getUserIdsWithArguments
from UserHistory.service import getHistoryFromId, getHistoryFromUserName,getHistoryFromIds
from ContentMetadata.service import getMetadataWithIds


def recommendBasedOnId(id):
    similarUsers = getNearestUsersWithId(id)

    if len(similarUsers)==0:
        return []

    similarIds = [data['_id'] for data in similarUsers]

    histories = getHistoryFromIds(similarIds)

    if len(histories['hits']['hits'])==0:
        return []
    
    histories = [data['_source']['history'] for data in histories['hits']['hits'] if data["_source"]["id"]!=id]
    # print(histories)
    recentlyWatched = [history[-1][0] for history in histories]
    movies = getMetadataWithIds(recentlyWatched)
    return movies

    