import numpy as np
import pandas as pd
import math

STRONG_BULL_SQN = 1.5
BULL_SQN = 0.7
NEUTRAL_SQN = 0
BEAR_SQN = -0.45


def sqn(df, period):
    if len(df.index) < period:
        raise Exception('Not enough data in data frame for period. Period=' + str(period) + ' Length=' + str(len(df.index)))

    title = 'SQN_' + str(period)
    #percent_change_df = (df - df.shift()) / df.shift()
    percent_change_df = df.pct_change(periods=1)
    avg_df = percent_change_df.rolling(window=period).mean()
    stdev_df = percent_change_df.rolling(window=period).std()

    multiplier = 0
    if period < 100:
        multiplier = math.sqrt(period)
    else:
        multiplier = 10

    sqn_df = (avg_df / stdev_df * multiplier).round(decimals=2)
    sqn_df.columns = [title]
    print(type(sqn_df))
    print(sqn_df.columns)
    return sqn_df


def categorize_sqn_market_type(df):
    sqn_list = df.swapaxes("index", "columns").to_numpy()[0]
    bins = [float('-inf'), BEAR_SQN, NEUTRAL_SQN, BULL_SQN, STRONG_BULL_SQN, float('inf')]
    labels = ["Strong Bear", "Bear", "Neutral", "Bull", "Strong Bull"]
    binned = pd.cut(sqn_list, bins=bins, labels=labels)
    return(binned)



data = [1,2,3,4,5,6,7,8,9]
df = pd.DataFrame(data)
sqn_df = sqn(df, 3)
print(sqn_df)
#classification_df = categorize_sqn_market_type(sqn_df)
#print(classification_df)