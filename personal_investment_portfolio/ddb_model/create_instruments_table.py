from __future__ import print_function # Python 2/3 compatibility
import boto3
import os

os.environ["TZ"] = "UTC"

dynamodb = boto3.resource('dynamodb', region_name='Oregon', endpoint_url="http://localhost:8000")

table = dynamodb.create_table(
    TableName='Instruments',
    KeySchema=[
        {
            'AttributeName': 'ticker',
            'KeyType': 'HASH'  #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ticker',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)