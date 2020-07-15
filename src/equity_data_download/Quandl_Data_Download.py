import quandl
import os
from datetime import datetime


START_DATE = "2018-12-01"
END_DATE = datetime.now().strftime('%Y-%m-%d')
quandl.ApiConfig.api_key = os.getenv('QUANDL_TOKEN')


def get_latest_commodity_prices_from_quandl():
    print("Processing Commodities")
    print("Processing: Gold")
    gold_df = quandl.get('LBMA/GOLD', start_date=START_DATE, end_date=END_DATE)
    gold_df.sort_index(ascending=False, inplace=True)
    gold_df['Commodity'] = 'Gold'
    commodity_df = gold_df.head(1)

    print("Processing: Silver")
    silver_df = quandl.get('LBMA/SILVER', start_date=START_DATE, end_date=END_DATE)
    silver_df.sort_index(ascending=False, inplace=True)
    silver_df['Commodity'] = 'Silver'
    silver_df = silver_df.head(1)
    commodity_df = commodity_df.append(silver_df, sort=True)

    return commodity_df

