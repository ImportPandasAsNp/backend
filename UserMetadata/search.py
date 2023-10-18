# from app import esclient
from es import esclient
from UserMetadata.mapping import indexName

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

    def build(self):
        return self.query

    def execute(self):
        res = client.search(index=indexName, body=self.query,size=1000)
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