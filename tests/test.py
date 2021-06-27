from iexfinance.stocks import get_historical_data, Stock
import pyEX as p
import os
from datetime import datetime
from pathlib import Path, PurePath
from instrument_data_access import pyex_dao as pyex

START_DATE = datetime(2016, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = PurePath(os.getcwd())
DATA_DIRECTORY = BASE_DIRECTORY / 'data'
EQUITY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY / "Portfolio_Instruments.csv"


#os.environ['IEX_API_VERSION'] = 'iexcloud-sandbox'
#os.environ['IEX_TOKEN'] = 'Tpk_ae6b710e445542509b3a4893c5ee3195'
os.environ['IEX_API_VERSION'] = 'v1'
#os.environ['IEX_TOKEN'] = 'sk_4b92debfe8f64518921d99dc030627a4'
os.environ['IEX_TOKEN'] = 'pk_1ce76a7935184dc2b0c08b79973e8287'
token  = os.environ['IEX_TOKEN']

print(token)

try:
    amzn_price = Stock("AMZN", token=token).get_price()
    print(amzn_price)
except Exception as e:
    print("IEX Query Error")




#token = 'pk_1ce76a7935184dc2b0c08b79973e8287'
#symbol = 'AMZN'
#c = p.Client(api_token=token)
#df = c.chartDF(symbol)
#c.yesterday(symbol)
#print(c.yesterdayDF(symbol))
#c.quote(symbol)
#df = c.pointsDF(symbol)
#df = c.chartDF(symbol, timeframe='5d')
#df = df[['open', 'close', 'high', 'low']].set_index(df['date'])
#print(df)
#df.head(5)

#pyex_downloader = pyex.pyex_dao()
#df = pyex_downloader.get_last_price(symbol)
#df = pyex_downloader.get_historical_price_data_for_instrument('AMZN')
#portfolio_last_price_dict = pyex_downloader.get_instruments_last_price_from_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME.as_posix())

#print(portfolio_last_price_dict)
