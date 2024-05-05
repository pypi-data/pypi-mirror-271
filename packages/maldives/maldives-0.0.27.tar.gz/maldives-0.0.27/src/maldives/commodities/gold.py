from maldives.regression import RegressionModel
from maldives.api import FredData
from maldives.backtest.utils import CalculateProbability, VisualizeProbability

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px


def load_gold_data(fred_api_key, start=pd.Timestamp.today()-pd.tseries.offsets.BDay(300), end=pd.Timestamp.today()):
    if type(start) is int:
            start = end - pd.tseries.offsets.BDay(start)

    # load gold futures prices
    gold = yf.Ticker("GC=F").history(start=start, end=end)
    gold.index = gold.index.date
    gold['ClosingPrice'] = gold['Close']
    gold = gold[['ClosingPrice']]

    # load cpi and treasury yield
    fred = FredData(fred_api_key)
    cpi, treasury = fred.CPI(), fred.Treasury10Y()

    df = pd.merge_asof(gold.join(
        treasury), cpi, left_index=True, right_index=True, direction='nearest')
    df = df.dropna().loc[start.date():end.date()]
    return df