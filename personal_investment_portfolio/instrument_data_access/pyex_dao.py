# https://pyex.readthedocs.io/en/latest/
import pyEX as p
import os
import pandas as pd
from instrument_data_access.data_access import data_access


class pyex_dao(data_access):

    def __init__(self):
        self.iex_token = 'pk_1ce76a7935184dc2b0c08b79973e8287'
        self.pyexClient = p.Client(api_token=self.iex_token)


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
                                                 instrument):
        print("pyex Processing: " + instrument)
        instrument_df = pd.DataFrame()

        try:
            instrument_df = self.pyexClient.chartDF(instrument, timeframe='5y')
            instrument_df = instrument_df.assign(Instrument=instrument)
            instrument_df.index.rename('Date', inplace=True)
        except Exception as e:
            print("pyex could not process " + instrument)
        return instrument_df


    def get_last_price(self, instrument):
        print("pyex processing: " + instrument)
        df = self.pyexClient.yesterdayDF(instrument)
        print(df['close'])
        return df
    

    def get_last_price_for_instrument_df(self, instruments_df):
        price_df = pd.DataFrame()
        try:
            price_df = self.pyexClient.yesterdayDF(instruments_df['Instrument'].values.tolist())
        except Exception as e:
            print("pyex Error")
        return price_df


    def get_instruments_last_price_from_csv_file(self, filename):
        instruments_df = super().get_instrument_list_from_csv(filename)
        return self.get_last_price_for_instrument_df(instruments_df)



