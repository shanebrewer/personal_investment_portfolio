from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from datetime import datetime, timedelta
import requests_cache
import pandas as pd
import time
import os
from pathlib import PurePath
from .data_importer import data_importer


class iex_data_importer(data_importer):

    def __init__(self):
        self.IEX_CLOUD_TOKEN = os.environ.get('IEX_TOKEN')
        self.START_DATE = datetime(2017, 1, 1)
        self.END_DATE = datetime.now()

        expiry = timedelta(days=3)
        self.session = requests_cache.CachedSession(cache_name='cache',
                                                   backend='sqlite',
                                                   expire_after=expiry)    


    def get_historical_price_data_for_instrument_list(self, 
                                                      instruments_df, 
                                                      start_date=self.START_DATE, 
                                                      end_date=self.END_DATE):
        instruments_price_data_df = pd.DataFrame()
        for row in instruments_df.itertuples():
            instrument_df = self.get_historical_price_data_for_instrument(getattr(row, 'Instrument'), start_date, end_date)
            instrument_df['Date'] = instrument_df.index.values
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
            time.sleep(self.SLEEP_PERIOD)
        return instruments_price_data_df


    def get_historical_price_data_for_instrument(self, 
                                                 instrument, 
                                                 start_date=self.START_DATE, 
                                                 end_date=self.END_DATE):
        print("Processing: " + instrument)
        try:
            instrument_df = get_historical_data(instrument,
                                                start=start_date,
                                                end=end_date,
                                                output_format='pandas')
            instrument_df = instrument_df.assign(Instrument=instrument)
        except Exception:
            print("Could not process " + instrument)
        return instrument_df


    def get_last_price(self, instrument):
        print("Processing: " + instrument)
        stock = Stock(instrument)
        return stock.get_price()


    def get_company_info(self, instrument):
        stock = Stock(instrument)
        return stock.get_company()


    def get_last_price_for_instrument_list(self, instruments_df):
        return Stock(instruments_df['Instrument'].values.tolist()).get_price()


    def get_historical_price_data_from_csv_file(self,
                                                filename, 
                                                start_date=self.START_DATE,
                                                end_date=self.END_DATE):
        instruments_df = super().read_equity_list_from_csv(filename)
        return self.get_historical_price_data_for_instrument_list(instruments_df, start_date, end_date)


    def get_company_info_from_csv_file(self, filename):
        instruments_df = super().read_equity_list_from_csv(filename)
        companies_info_df = pd.DataFrame()

        for row in instruments_df.itertuples():
            company_info_df = self.get_company_info(getattr(row, 'Instrument'))
            # TODO: Aggregate to list here
            
        return companies_info_df

    def get_last_prices_from_instruments_in_csv_file(self, filename):
        instruments_df = super().read_equity_list_from_csv(filename)
        return self.get_last_price_for_instrument_list(instruments_df)


