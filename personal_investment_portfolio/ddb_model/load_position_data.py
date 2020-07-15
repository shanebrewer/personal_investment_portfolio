from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

PATH = "d:\\Users\\Shane\\OneDrive\\Repositories\\Investing\\Investment Portfolio Dashboard\\data\\"

dynamodb = boto3.resource('dynamodb', region_name='Oregon', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Positions')

with open(PATH + "positions.json") as json_file:
    instruments = json.load(json_file, parse_float = decimal.Decimal)
    for instrument in instruments:
        ticker = instrument['ticker']
        info = instrument['info']

        print("Adding position:", ticker)

        table.put_item(
           Item={
               'ticker': ticker,
               'info': info,
            }
        )