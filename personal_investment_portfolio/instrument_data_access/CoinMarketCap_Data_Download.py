from coinmarketcap.clients import CoinMarketCapClient
from pathlib import PurePath
import pandas as pd
import time
import os


BASE_DIRECTORY = PurePath(os.getcwd())
DATA_DIRECTORY = BASE_DIRECTORY.parents[2] / "data"
INPUT_DATA_FILENAME = DATA_DIRECTORY / "CoinMarketCapCryptocurrencyIDs.csv"
SLEEP_PERIOD = 5
client = CoinMarketCapClient()


def get_cryptocurrency_list_from_csv(filename_and_path):
    print("Reading data file: " + filename_and_path)
    df = pd.read_csv(filename_and_path)
    return df


def get_cryptocurrency_list_from_coinmarketcap():
    return(client.listing.get())


def get_latest_cryptocurrency_portfolio_prices_from_coinmarketcap(filename_and_path=INPUT_DATA_FILENAME):
    instruments_df = get_cryptocurrency_list_from_csv(filename_and_path)
    instruments_price_data_df = pd.DataFrame()

    for row in instruments_df.itertuples():
        instrument = getattr(row, 'id')
        instrument_name = getattr(row, 'name')
        print("Processing: " + instrument_name)

        try:
            instrument_df = pd.DataFrame.from_dict(client.cryptocoin.get(coin_id=instrument))
            latest_price = instrument_df['quotes']['USD']['price']
            instrument_df['Last Price'] = latest_price
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True, sort=True)
            time.sleep(SLEEP_PERIOD)
        except:
            print("Error when processing: " + instrument_name)
    return instruments_price_data_df
