import quandl
import os
from datetime import datetime
from instrument_data_access.data_access import data_access


class quandl_dao(data_access):

    def __init__(self):
        self.START_DATE = "2017-01-01"
        self.END_DATE = datetime.now().strftime('%Y-%m-%d')
        quandl.ApiConfig.api_key = os.environ.get('QUANDL_TOKEN')


    def get_latest_commodity_prices_from_quandl(self):
        print("Processing Commodities")
        commodity_df = self.get_latest_gold_price_from_quandl()
        commodity_df = commodity_df.append(self.get_latest_silver_price_from_quandl())
        return commodity_df


    def get_latest_gold_price_from_quandl(self):
        gold_df = self.get_latest_instrument_price_from_quandl('LBMA/GOLD')
        gold_df['Commodity'] = 'Gold'
        return gold_df
        

    def get_latest_silver_price_from_quandl(self):
        silver_df = self.get_latest_instrument_price_from_quandl('LBMA/SILVER')
        silver_df['Commodity'] = 'Silver'
        return silver_df

    def get_latest_instrument_price_from_quandl(self, instrument):
        print("Processing: " + instrument)
        instrument_df = quandl.get(instrument, rows=1)
        instrument_df.sort_index(ascending=False, inplace=True)
        return instrument_df
    

    def get_instrument_historical_prices_from_quandl(self, instrument, start_date, end_date):
        print("Processing: " + instrument)
        instrument_df = quandl.get(instrument, start_date=start_date, end_date=end_date)
        instrument_df.sort_index(ascending=False, inplace=True)
        return instrument_df