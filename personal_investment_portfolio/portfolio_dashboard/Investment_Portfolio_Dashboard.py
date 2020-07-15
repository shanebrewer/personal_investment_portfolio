import os
#from data_import.CoinMarketCap_Data_Download import *
#from data_import.data_importer import *
import pandas as pd
import boto3
import json
import decimal
from data_import.IEX_Data_Download import *
from data_import.Quandl_Data_Download import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb', region_name='Oregon', endpoint_url="http://localhost:8000")


def load_positions():
    positions_table = dynamodb.Table('Positions')

    print("Loading Positions from DDB")

    positions = positions_table.scan()
    for i in positions['Items']:
        print(i['ticker'], ":", i['info']['quantity'])
    
    return positions


def generate_html_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def main():
    pd.options.display.float_format = '${:,.2f}'.format
    positions = load_positions()
    
    instruments_table = dynamodb.Table('Instruments')
    columns_list = ['Ticker', 'Quantity', 'Price', 'Total Value']
    portfolio_data_list = []

    for i in positions['Items']:
        ticker = i['ticker']
        response = instruments_table.query(KeyConditionExpression=Key('ticker').eq(ticker))
        item = response['Items'][0]
        quantity = int(i['info']['quantity'])
        
        if(item['info']['instrument_type'] == "Stock" or item['info']['instrument_type'] == "ETF"):
            price = float(get_last_price_from_iex(ticker))
            portfolio_data_list.append([ticker, quantity, price, quantity * price])
        elif(item['ticker'] == 'XAUUSD'):
            gold_price_df = get_latest_gold_price_from_quandl()
            price = float(gold_price_df.iloc[0]["USD (AM)"])
            portfolio_data_list.append([ticker, quantity, price, quantity * price])
        elif(item['ticker'] == 'XAGUSD'):
            silver_price_df = get_latest_silver_price_from_quandl()
            price = float(silver_price_df.iloc[0]['USD'])
            portfolio_data_list.append([ticker, quantity, price, quantity * price])

    portfolio_positions_df = pd.DataFrame(portfolio_data_list, columns=columns_list)
    portfolio_positions_df['Price'] = portfolio_positions_df['Price'].map('${:,.2f}'.format)
    portfolio_positions_df['Total Value'] = portfolio_positions_df['Total Value'].map('${:,.2f}'.format)
    
    print(portfolio_positions_df)

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div(children=[
        html.H4(children='Portfolio'),
        generate_html_table(portfolio_positions_df)
    ])

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
