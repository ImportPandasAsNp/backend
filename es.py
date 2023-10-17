import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch,RequestsHttpConnection
from requests_aws4auth import AWS4Auth

load_dotenv()
awsAccessKey = os.getenv("awsAccessKey")
awsSecretKey = os.getenv("awsSecretKey")
regionName = os.getenv("regionName") 
domainName = os.getenv("domainName")

# basicAuth = f"{awsAccessKey}:{awsSecretKey}"

awsauth = AWS4Auth(awsAccessKey, awsSecretKey, regionName, "es")

def connectToEs():
    es = Elasticsearch(timeout=120, max_retries=10,
        hosts = [{'host': domainName, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection)
    print("Es connected successfully")
    print(es.ping)
    return es

class ESclient:
    def __init__(self) -> None:
        self.client = None
    
    def getClient(self):
        if self.client is None:
            self.client = connectToEs()
        
        return self.client