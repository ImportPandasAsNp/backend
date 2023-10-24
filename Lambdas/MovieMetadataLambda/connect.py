from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import os

awsAccessKey = os.environ["ACCESS_KEY"]
awsSecretKey = os.environ["SECRET_KEY"]
regionName = "ap-south-1"  
domainName = os.environ["URL"]

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