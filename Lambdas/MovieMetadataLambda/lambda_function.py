import json
import urllib.parse
import boto3
import csv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch import helpers
from connect import connectToEs

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
            cast = "".join(data[i]["cast"])
            genre = "".join(data[i]["genre"])
            source = {
                        'type':data[i]['type'],
                        'title':data[i]['title'],
                        'director':data[i]['director'],
                        'cast':cast,
                        'country':data[i]['country'],
                        'release_year':data[i]['release_year'],
                        'age_rating':data[i]['rating'],
                        'imdb_rating':data[i]['imdb_rating'],
                        'genre':genre,
                        'platform':data[i]['platform'],
                        'id':data[i]['id'],
                        'image_url':data[i]['image_url'],
                        'description':data[i]['description']
                     }
                     
            action = {
                        '_index': 'moviemetadata1',
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
            data_dict[row_number] = row_data

        print("Storing")
        bulk(data_dict)
        print("Stored")

    except Exception as e:
        return {
            'statusCode':500,
            'body':str(e)
        }
    
