# https://docs.intrinio.com/documentation/python

from instrument_data_access.data_access import data_access
import pandas as import pd
import intrinio_sdk
from datetime import datetime


class intrinio_dao(data_access):

    def __init__(self):
        self.START_DATE = "2017-01-01"
        self.END_DATE = datetime.now().strftime('%Y-%m-%d')
        intrinio_sdk.ApiClient().configuration.api-key['api_key'] = os.environ.get('INTRINIO_API_KEY')
        security_api = intrinio_sdk.security_api()


    def get_instrument_historical_prices(self, instrument, start_date, end_date):
        print("Intinio Finance Processing: " + instrument)
        instrument_data = security_api.get_security_stock_prices(identifier=instrument, start_date=start_date, end_date=end_date, frequency='daily')
        response_list = [x.to_dict() for x in instrument_data.stock_prices]
        instrument_df = pd.DataFrame(response_list).sort_values('date')
        instrument_df.set_index('date', inplace=True)
        return instrument_df