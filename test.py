from Utils.api import createIndex,createMapping,createSetting,closeIndex,openIndex,deleteIndex,insertRecord,getAllRecords,deleteAllRecords,getRecord
from UserFeatures.mapping import featureMapping,featureSetting,indexName as featureIndex
from UserMetadata.mapping import metadataMapping,indexName as metadataIndex, dummyUser,dummyUser1
from ContentFeatures.service import getFeaturesWithContentName
from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId,getFeaturesWithId
from UserHistory.mapping import historyMapping, indexName as historyIndex
from UserHistory.update import updateHistory, updateUserFeature
from Recommendation.contentbased import recommendBasedOnId,recommendBasedOnName
from ContentMetadata.service import getMetadataWithIds as movie
from Recommendation.collaborative import recommendBasedOnId as collabId
from UserHistory.service import getHistoryFromNames,getHistoryFromIds


if __name__ == "__main__":
    # deleteAllRecords(historyIndex)
    # deleteIndex(historyIndex)
    # createIndex(historyIndex)
    # createMapping(historyIndex,historyMapping)
    # insertRecord(historyIndex,{
    #     "id":"123456",
    #     "history":[['1','2'],['2','3']]
    # })
    # print(getRecord(historyIndex,'123456'))
    # updateHistory('123456',['4','5'])
    # print(getFeaturesWithId('123456')[0])
    # print(updateUserFeature('123456', ['13644510926972048555',3]))
    # time.sleep(2)
    # print(getFeaturesWithId('123456')[0])
    # print(recommendBasedOnId('123456',{
    #     'country':'United States'
    # }))
    # print(movie(['13644510926972048555']))
    # updateHistory('234567',['1','2'])
    # print(getAllRecords("user_metadata",size=3))
    print(getHistoryFromNames(["Aditya","amartya"]))