import pandas as pd
import math


def ndx(df, period):
    if len(df.index) < period:
        raise Exception('Not enough data in data frame for period')

    # Formula: Price - Lowest Low(n)/(Highest High(n) - Lowest Low(n)) * 100
    min_price_df = df["low"].rolling(window=period).min().shift(1)
    max_price_df = df["high"].rolling(window=period).max().shift(1)
    ndx_df = ((df["close"] - min_price_df) / (max_price_df - min_price_df) * 100).round(decimals=1)
    return ndx_df