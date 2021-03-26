import pandas as pd


VERY_VOLATILE_ATR = 3.5
VOLATILE_ATR = 1.65
NORMAL_ATR = 1


def atr(df):
    atr_df = pd.DataFrame()
    atr_df['ATR1'] = abs(df['high'] - df['low'])
    atr_df['ATR2'] = abs(df['high'] - df['close'].shift())
    atr_df['ATR3'] = abs(df['low'] - df['close'].shift())
    atr_df['TrueRange'] = atr_df[['ATR1', 'ATR2', 'ATR3']].max(axis=1)
    return atr_df['TrueRange']


def atr_percent_of_close(df, period):
    df['ATR'] = atr(df)
    df['ATR_Percent_Of_Close'] = df['ATR'] / df['close'] * 100
    return df['ATR_Percent_Of_Close'].rolling(window=period).mean().round(decimals=2)


def classify_atr_market_type(df):
    atr_list = df.swapaxes("index", "columns").to_numpy()[0]
    bins = [float('-inf'), NORMAL_ATR, VOLATILE_ATR, VERY_VOLATILE_ATR, float('inf')]
    labels = ["Quiet", "Normal", "Volatile", "Very Volatile"]
    binned = pd.cut(atr_list, bins=bins, labels=labels)
    return(binned)