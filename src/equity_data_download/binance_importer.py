from binance.client import Client, BinanceAPIException
from datetime import datetime
from pathlib import PurePath
import pandas as pd
import os
from .data_importer import data_importer

BASE_DIRECTORY = PurePath(os.getcwd())
DATA_DIRECTORY = BASE_DIRECTORY.parents[2] / "data"
INPUT_DATA_FILENAME = DATA_DIRECTORY / "Binance_Instruments.csv"
START_DATE_DEFAULT = datetime(2019, 1, 1)
END_DATE_DEFAULT = datetime.now()


class binance_data_importer(data_importer):
    def __init__(self):
        self.api_key = os.environ.get('BINANCE_API_KEY')
        self.api_secret = os.environ.get('BINANCE_SECRET_KEY')
        self.client = Client(self.api_key, self.api_secret)
    

    def get_historical_price_data_for_instrument_list(self, instruments_df, start_date=START_DATE_DEFAULT, end_date=END_DATE_DEFAULT):
        instruments_price_data_df = pd.DataFrame()
        for row in instruments_df.itertuples():
            instrument_df = self.get_historical_price_data_for_instrument(getattr(row, 'Instrument'), start_date, end_date)
            instruments_price_data_df = instruments_price_data_df.append(instruments_df, ignore_index=True, sort=True)
        return instruments_price_data_df


    def get_historical_price_data_for_instrument(self, instrument, start_date=START_DATE_DEFAULT, end_date=END_DATE_DEFAULT):
        print("Processing: " + instrument)
        try:
            instrument_prices = self.client.get_historical_klines(symbol=instrument, interval='1d', start_str=start_date.strftime('%m/%d/%Y'))
            instrument_prices_df = pd.DataFrame(instrument_prices, columns = ['Open_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_Time', 'Quote_Asset_Volume', 'Num_Trades', 'Taker_Buy_Base_Volume', 'Taker_Buy_Quote_Volume', 'Ignore'])
            instrument_prices_df['Date'] = pd.to_datetime(instrument_prices_df['Open_Time'], unit='ms')
            instrument_prices_df = instrument_prices_df.assign(Instrument=instrument)
            instrument_prices_df = instrument_prices_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Instrument']]
        except BinanceAPIException:
            print("BinanceAPIException thrown for " + instrument)
        except Exception:
            print("Could not process " + instrument)
        return instrument_prices_df


    def get_last_price(self, instrument):
        print("Processing: " + instrument)
        try:
            price = (self.client.get_ticker(symbol=instrument))['lastPrice']
        except Exception:
            print("Could not process " + instrument)
        return price


    def get_last_prices_from_instruments_in_csv_file(self, filename):
        instruments_df = super().read_equity_list_from_csv(filename)
        return self.get_last_price_for_instrument_list(instruments_df)
    

    def get_historical_price_data_from_csv_file(self, filename, start_date=START_DATE_DEFAULT, end_date=END_DATE_DEFAULT):
        instruments_df = super().read_equity_list_from_csv(filename)
        return self.get_historical_price_data_for_instrument_list(instruments_df)