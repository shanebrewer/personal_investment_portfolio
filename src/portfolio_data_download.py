import sys
import os
import logging
from  equity_data_download import IEX_Data_Download as eq
from equity_data_download import CoinMarketCap_Data_Download as cmc
from equity_data_download import binance_importer as bi
from equity_data_download import Quandl_Data_Download as qdl
#from data_import.IEX_Data_Download import *
#from .data_import.CoinMarketCap_Data_Download import *
#from .data_import.Quandl_Data_Download import *
#from .data_import.data_importer import *
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
    iex_downloader = eq.iex_data_importer()
    portfolio_last_price_dict = iex_downloader.get_last_prices_from_instruments_in_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME.as_posix())
    portfolio_last_price_df = pd.DataFrame.from_dict([portfolio_last_price_dict])
    portfolio_historical_price_df = iex_downloader.get_historical_price_data_from_csv_file(EQUITY_PORTFOLIO_CSV_FILENAME.as_posix(),
                                                                                           START_DATE,
                                                                                           END_DATE)
    
    # Download Crypto prices
    #cryptocurrency_last_price_df = \
    #    cmc.get_latest_cryptocurrency_portfolio_prices_from_coinmarketcap(CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME.as_posix())
    binanace_downloader = bi.binance_data_importer()
    cryptocurrency_historical_price_df = binanace_downloader.get_historical_price_data_from_csv_file(CRYPTOCURRENCY_PORTFOLIO_CSV_FILENAME.as_posix())

    # Download Commodity Prices
    commodity_df = qdl.get_latest_commodity_prices_from_quandl()

    write_excel_file(portfolio_last_price_df,
                     portfolio_historical_price_df,
                     cryptocurrency_historical_price_df,
                     commodity_df)
