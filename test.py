from Utils.api import createIndex,createMapping,createSetting,closeIndex,openIndex,deleteIndex,insertRecord,getAllRecords,deleteAllRecords,getRecord
from UserFeatures.mapping import featureMapping,featureSetting,indexName as featureIndex
from UserMetadata.mapping import metadataMapping,indexName as metadataIndex, dummyUser,dummyUser1
from ContentFeatures.service import getFeaturesWithContentName
from UserFeatures.service import getNearestUsersWithUserName,getNearestUsersWithId,getFeaturesWithId
from UserHistory.mapping import historyMapping, indexName as historyIndex
from UserHistory.update import updateHistory, updateUserFeature
import time


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
    print(getFeaturesWithId('123456')[0])
    print(updateUserFeature('123456', ['13644510926972048555',3]))
    time.sleep(2)
    print(getFeaturesWithId('123456')[0])