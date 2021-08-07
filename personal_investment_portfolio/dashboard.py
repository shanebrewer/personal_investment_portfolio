# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Load Portfolio Positions

# %%
import os
import pandas as pd
import decimal
from instrument_data_access.IEX_dao import *
from instrument_data_access.quandl_dao import *
from instrument_data_access.binance_dao import *
from pathlib import Path, PurePath
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


# Constants
BASE_DIRECTORY = PurePath(os.getcwd())
DATA_DIRECTORY = BASE_DIRECTORY / 'data'
PORTFOLIO_POSITIONS_FILE = DATA_DIRECTORY / 'positions.csv'

iex_data_importer = iex_dao()
quandl_data_importer = quandl_dao()
binance_data_importer = binance_dao()

# Load Portfolio Positions
positions_df = pd.read_csv(PORTFOLIO_POSITIONS_FILE.as_posix())
print(positions_df)

# %% [markdown]
# # Filter Equities

# %%

index_list = []
for row_index, row in positions_df.iterrows():
    if(row['Type'] == "ETF") or (row['Type'] == 'Stock'):
        index_list.append(row['Instrument'])
print(index_list)
index_pd = pd.DataFrame(index_list, columns=['Instrument'])
print(index_pd)

# %% [markdown]
# # Get Last Prices for Equities

# %%
last_price_df = pd.DataFrame()

for row_index, row in positions_df.iterrows():
    if(row['Type'] == "ETF") or (row['Type'] == 'Stock'):
        last_price = iex_data_importer.get_last_price(row['Instrument']).iloc[0,0]
        df = {'Last_Price': last_price}
        last_price_df = last_price_df.append(df, ignore_index=True)
    elif (row['Type'] == "Commodity"):
        last_price = quandl_data_importer.get_latest_instrument_price(row['Instrument']).iloc[0,0]
        df = {'Last_Price': last_price}
        last_price_df = last_price_df.append(df, ignore_index=True)
    elif (row['Type'] == "Cryptocurrency"):
        last_price = binance_data_importer.get_last_price(row['Instrument'])
        df = {'Last_Price': last_price}
        last_price_df = last_price_df.append(df, ignore_index=True)

# TODO: Add an index and merge data frames together

positions_df = positions_df.assign(Last_Price=last_price_df)
positions_df

# %% [markdown]
# # Calculate Total Assets

# %%

def currency_format(x):
    return "${0:,.2f}".format(x)

positions_df['Total_Assets'] = positions_df['Quantity'].astype(int) * positions_df['Last_Price'].astype(float)
positions_df['Total_Assets'] = positions_df['Total_Assets'].apply(currency_format)
positions_df['Last_Price'] = positions_df['Last_Price'].astype(float).apply(currency_format)
positions_df


# %%

instruments_info_dict = {}

for row_index, row in positions_df.iterrows():
    if (row['Type'] == "ETF") or (row['Type'] == 'Stock'):
        instrument = row['Instrument']
        instrument_info_dict = iex_data_importer.get_company_info(instrument)
        instruments_info_dict[instrument] = instrument_info_dict
    


print(instruments_info_dict)


# %%
crypto_last_prices = binance_data_importer.client.get_symbol_ticker(symbol='XRPUSDT')
print(crypto_last_prices)


# %%
quandl_data_importer.get_latest_instrument_price('LBMA/GOLD').iloc[0][0]


# %%
positions_df


# %%



