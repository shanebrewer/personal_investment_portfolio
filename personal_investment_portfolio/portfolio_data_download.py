import sys
import os
import logging
from instrument_data_access import iex_dao as eq
from instrument_data_access import binance_dao as bi
from instrument_data_access import quandl_dao as qdl
from pathlib import Path, PurePath
import pandas as pd
from datetime import datetime


START_DATE = datetime(2017, 1, 1)
END_DATE = datetime.now()
TODAY_DATE = datetime.now().strftime('%m-%d-%Y')
BASE_DIRECTORY = PurePath(os.getcwd())
DATA_DIRECTORY = BASE_DIRECTORY / 'data'
EQUITY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY / "Portfolio_Instruments.csv"
#CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY / "CoinMarketCap_Cryptocurrency_IDs.csv"
CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME = DATA_DIRECTORY / "Binance_Instruments.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY / 'output'
OUTPUT_EXCEL_FILENAME = OUTPUT_DIRECTORY / 'portfolio_data.xlsx'


def write_excel_file(last_df, historical_df, cryptocurrency_last_price_df, commodity_df):
    logging.info("Writing Excel File: " + OUTPUT_EXCEL_FILENAME.as_posix())
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME.as_posix())
    last_df.to_excel(writer, 'Last Day')
    historical_df.to_excel(writer, 'Historical')
    cryptocurrency_last_price_df.to_excel(writer, 'Cryptocurrency')
    commodity_df.to_excel(writer, 'Commodities')
    writer.save()


def check_write_file_permissions():
    try:
        with open(OUTPUT_EXCEL_FILENAME, 'w') as file:
            logging.info('Output file has write permissions')
    except IOError as ex:
        logging.error('Output file ' + str(OUTPUT_EXCEL_FILENAME) + ' is not writable. Exiting.')
        raise SystemExit


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    check_write_file_permissions()
    
    # Download Equity prices
    iex_downloader = eq.iex_dao()
    portfolio_last_price_dict = iex_downloader.get_instruments_last_price_from_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME.as_posix())
    portfolio_last_price_df = pd.DataFrame.from_dict([portfolio_last_price_dict])
    portfolio_historical_price_df = iex_downloader.get_instruments_historical_prices_from_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME.as_posix(),
                                                                                                   START_DATE,
                                                                                                   END_DATE)
    
    # Download Crypto prices
    #cryptocurrency_last_price_df = \
    #    cmc.get_latest_cryptocurrency_portfolio_prices_from_coinmarketcap(CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME.as_posix())
    binanace_downloader = bi.binance_dao()
    cryptocurrency_historical_price_df = binanace_downloader.get_historical_price_data_from_csv_file(CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME.as_posix(),
                                                                                                     START_DATE,
                                                                                                     END_DATE)

    # Download Commodity Prices
    quandl_downloader = qdl.quandl_dao()
    commodity_df = quandl_downloader.get_latest_commodity_prices_from_quandl()

    write_excel_file(portfolio_last_price_df,
                     portfolio_historical_price_df,
                     cryptocurrency_historical_price_df,
                     commodity_df)
