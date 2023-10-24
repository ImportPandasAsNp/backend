import json
import urllib.parse
import boto3
import csv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers
from connect import connectToEs
import json

s3 = boto3.client("s3")
client = connectToEs()

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    saveSize = 50
    
    def bulk(data):
        keys = list(data.keys())
        actions = []
    
        for i in keys:
            print(i)

            source = {
                        'feature':data[i]['feature'],
                        'id':data[i]['id']
                     }
                     
            action = {
                        '_index': 'moviefeatures',
                        '_op_type': 'index',
                        '_id': data[i]['id'],
                        '_source': source
                     }
            
            
            actions.append(action)
            print(action)
            if len(actions) >= saveSize:
                helpers.bulk(client, actions)
                del actions[0:len(actions)]

        if len(actions) > 0:
            helpers.bulk(client, actions)
            
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        csv_content = response['Body'].read().decode('utf-8')   
        
        data_dict = {}

        csv_reader = csv.reader(csv_content.strip().split('\n'))

        headers = next(csv_reader)

        for row_number, row in enumerate(csv_reader, start=1):
            row_data = {headers[i]: value for i, value in enumerate(row)}
            row_data["feature"] = json.loads(row_data["feature"])
            data_dict[row_number] = row_data
        
        bulk(data_dict)

    except Exception as e:
        return {
            'statusCode':500,
            'body':str(e)
        }
    