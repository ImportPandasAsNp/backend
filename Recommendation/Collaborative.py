from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId
from ContentFeatures.service import getKNNMetadataWithFeature,getFeaturesWithId as getMovieFeaturesWithId
from UserMetadata.service import getIdsWithArguments as getUserIdsWithArguments
from UserHistory.service import getHistoryFromId, getHistoryFromUserName,getHistoryFromIds
from ContentMetadata.service import getMetadataWithIds
from Utils.AgeRating import ageRatingList

def filterByAgeRating(metadata,queryDict):
    ratingList = ageRatingList(queryDict['rating'])
    return metadata["_source"]["age_rating"] in ratingList

def filterBySubscribedPlatforms(metadata,queryDict):
    platforms = queryDict["subscribed_platforms"]
    return metadata["_source"]["platform"] in platforms
    
def recommendBasedOnId(id, queryDict=None,returnFeatures=False):
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
    movies = filter(lambda x:filterByAgeRating(x,queryDict),movies)
    movies = filter(lambda x:filterBySubscribedPlatforms(x,queryDict),movies)

    if returnFeatures:
        for data in movies:
            data['feature'] = getMovieFeaturesWithId(data["_id"])
    return movies

    