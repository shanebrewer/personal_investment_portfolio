from instrument_data_access.data_access import data_access
import pandas as import pd
import yfinance as yf
from datetime import datetime


class yfinance_dao(data_access):

    def __init__(self):
        self.START_DATE = "2017-01-01"
        self.END_DATE = datetime.now().strftime('%Y-%m-%d')


    def get_instrument_historical_prices(self, instrument, start_date, end_date):
        print("Yahoo Finance Processing: " + instrument)
        instrument_df = yf.download(instrument, start=start_date, end=end_date, progress=False)
        instrument_df.sort_index(ascending=False, inplace=True)
        return instrument_df