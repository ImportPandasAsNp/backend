# from app import esclient
from es import esclient
from ContentMetadata.mapping import indexName
from Utils.AgeRating import ageRatingList
from Utils.constants import PLATFORMS

esclient.getClient()
client = esclient.client
aws4auth = esclient.aws_auth_client

class QueryBuilder:
    def __init__(self):
        self.query = {
            "query": {
                "bool":{
                    "must":[]
                }
            }
        }

        # client = esclient.client
        # aws4auth = esclient.aws_auth_client

    @staticmethod
    def builder():
        return QueryBuilder()

    def addQuery(self, key, names):
        if isinstance(names, list):
            names = " ".join(names)

        self.query["query"]["bool"]["must"].append({
            "match":{
                key:{
                    "query":names,
                    "operator":"and"
                }
            }
        })

        return self
    
    def addRatingQuery(self,rating):
        if rating!="A":
            self.query['query']['bool']["must"].append({
                "terms":{
                    "age_rating":ageRatingList(rating)
                }
            })

    def addPlatformsQuery(self,platformList):
        if len(platformList)<len(PLATFORMS):
            print(platformList)
            self.query['query']['bool']["must"].append({
                "terms":{
                    "platform":platformList
                }
            })

    def addPlotQuery(self,queryText):
        self.query['query']['bool']['should']=list()
        self.query['query']['bool']['should'].append({
            'match':{
                'plot':{
                    'query':queryText,
                    'minimum_should_match':'90%'
                }
            }
        })

    def build(self):
        return self.query

    def execute(self):
        res = client.search(index=indexName, body=self.query,size=5000)
        return res
   

def getIds(idList):
    print("search", client, aws4auth)
    query = {
        "query":{
            "ids":{
                "values":idList
            }
        }
    }

    return client.search(index = indexName, body=query)



# if __name__=="__main__":
#     rec= getIds(['10282685235321149091'])
#     print(rec)