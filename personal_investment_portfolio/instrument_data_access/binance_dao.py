from binance.client import Client, BinanceAPIException
from datetime import datetime
import pandas as pd
import os
import time
from instrument_data_access.data_access import data_access


class binance_dao(data_access):
   
    
    def __init__(self):
        self.api_key = os.environ.get('BINANCE_API_KEY')
        self.api_secret = os.environ.get('BINANCE_SECRET_KEY')
        self.client = Client(self.api_key, self.api_secret)
    

    def get_historical_price_data_for_instrument_list(self, instruments_df, start_date, end_date):
        instruments_price_data_df = pd.DataFrame()
        for row in instruments_df.itertuples():
            instrument_df = self.get_historical_price_data_for_instrument(getattr(row, 'Instrument'), start_date, end_date)
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
        return instruments_price_data_df


    def get_historical_price_data_for_instrument(self, instrument, start_date, end_date):
        print("Binance processing: " + instrument)
        try:
            instrument_prices = self.client.get_historical_klines(symbol=instrument, interval='1d', start_str=start_date.strftime('%m/%d/%Y'))
            instrument_prices_df = pd.DataFrame(instrument_prices, columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 'Num_Trades', 'Taker_Buy_Base_Volume', 'Taker_Buy_Quote_Volume', 'Ignore'])
            instrument_prices_df['Date'] = pd.to_datetime(instrument_prices_df['Open_Time'], unit='ms')
            instrument_prices_df = instrument_prices_df.assign(Instrument=instrument)
            instrument_prices_df = instrument_prices_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Instrument']]
            time.sleep(1)
        except BinanceAPIException:
            print("BinanceAPIException thrown for " + instrument)
        except Exception:
            print("Could not process " + instrument)
        return instrument_prices_df


    def get_last_price_for_instrument_list(self, instruments_df):
        instruments_price_data_df = pd.DataFrame()
        for row in instruments_df.itertuples():
            instrument_df = self.get_last_price(getattr(row, 'Instrument'))
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
        return instruments_price_data_df


    def get_last_price(self, instrument):
        print("Binance processing: " + instrument)
        try:
            price = (self.client.get_symbol_ticker(symbol=instrument))['price']
            time.sleep(1)
        except Exception:
            print("Could not process " + instrument)
        return price


    def get_last_prices_from_instruments_in_csv_file(self, filename):
        instruments_df = super().get_instrument_list_from_csv(filename)
        return self.get_last_price_for_instrument_list(instruments_df)
    

    def get_historical_price_data_from_csv_file(self, filename, start_date, end_date):
        instruments_df = super().get_instrument_list_from_csv(filename)
        return self.get_historical_price_data_for_instrument_list(instruments_df, start_date, end_date)