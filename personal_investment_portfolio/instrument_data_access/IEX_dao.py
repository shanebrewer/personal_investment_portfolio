from iexfinance.stocks import get_historical_data, Stock
import requests_cache
from datetime import datetime, timedelta
import pandas as pd
import time
from instrument_data_access.data_access import data_access


class iex_dao(data_access):

    def __init__(self):
        
        expiry = timedelta(days=7)
        self.session = requests_cache.CachedSession(cache_name='cache',
                                                   backend='sqlite',
                                                   expire_after=expiry)    


    def get_historical_price_data_for_instrument_df(self, 
                                                    instruments_df, 
                                                    start_date, 
                                                    end_date):
        instruments_price_data_df = pd.DataFrame()
        for row in instruments_df.itertuples():
            instrument_df = self.get_historical_price_data_for_instrument(getattr(row, 'Instrument'), start_date, end_date)
            instrument_df['Date'] = instrument_df.index.values
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
        return instruments_price_data_df


    def get_historical_price_data_for_instrument(self, 
                                                 instrument,
                                                 start_date, 
                                                 end_date):
        print("IEX Processing: " + instrument)
        instrument_df = pd.DataFrame()

        try:
            instrument_df = get_historical_data(instrument,
                                                start=start_date, 
                                                end=end_date,
                                                #session=self.session,
                                                close_only=True,
                                                output_format='pandas')
            instrument_df = instrument_df.assign(Instrument=instrument)
        except Exception as e:
            print("Could not process " + instrument)
        return instrument_df


    def get_instruments_last_price_from_csv_file(self, filename):
        instruments_df = super().get_instrument_list_from_csv(filename)
        return self.get_last_price_for_instrument_df(instruments_df)


    def get_last_price_for_instrument_df(self, instruments_df):
        price_df = pd.DataFrame()
        try:
            price_df = Stock(instruments_df['Instrument'].values.tolist(), session=self.session).get_price()
        except Exception as e:
            print("IEX Query Error")
        return price_df


    def get_last_price(self, instrument):
        print("IEX Processing: " + instrument)
        stock = Stock(instrument, session=self.session)
        return stock.get_price()


    def get_company_info(self, instrument):
        stock = Stock(instrument, session=self.session)
        return stock.get_company()


    def get_instruments_historical_prices_from_csv_file(self,
                                                filename, 
                                                start_date,
                                                end_date):
        instruments_df = super().get_instrument_list_from_csv(filename)
        return self.get_historical_price_data_for_instrument_df(instruments_df, start_date, end_date)


    def get_company_info_from_csv_file(self, filename):
        instruments_df = super().get_instrument_list_from_csv(filename)
        companies_info_df = pd.DataFrame()

        for row in instruments_df.itertuples():
            company_info_df = self.get_company_info(getattr(row, 'Instrument'))
            # TODO: Aggregate to list here
            
        return companies_info_df



