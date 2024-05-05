from maldives.regression import LinearRegressor
from maldives.api.usda import CattleWeeklyProduction
from maldives.api import FredData
from maldives.backtest.utils import CalculateProbability, VisualizeProbability

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px


class CattlePriceModel(object):
    def __init__(self, shift=4):
        self.df = None
        self.fitted = False

        self.model = LinearRegressor(transform=np.log, invtransform=np.exp)
        self.last_date = None
        self.current_price = np.nan
        self.prob = None
        self.uncertainty = None
        self.shift = shift

    def load_data(self, fred_api_key, start=pd.Timestamp.today()-pd.tseries.offsets.BDay(300), end=pd.Timestamp.today()):
        if type(start) is int:
            start = end - pd.tseries.offsets.BDay(start)

        # load gold futures prices
        days_back_required = (pd.Timestamp.today()-start).round('D').days
        df_cattle = CattleWeeklyProduction().load_data(days_back_required/5+4)

        cattle = yf.Ticker("LE=F").history(start=start, end=end)
        cattle['Date'] = pd.to_datetime(cattle['Date'])
        cattle['ClosingPrice'] = cattle['Close']
        cattle = cattle.set_index('Date')[['ClosingPrice']]
        self.current_price = cattle.ClosingPrice.values[-1]

        # load cpi and treasury yield
        fred = FredData(fred_api_key)
        cpi = fred.CPI()

        df = pd.merge_asof(cattle, cpi, left_index=True,
                           right_index=True, direction='nearest')
        df = pd.merge_asof(df_cattle, df, left_index=True,
                           right_index=True, direction='forward')

        df = df.dropna().loc[start.date():end.date()]
        self.df = df
        self.last_date = self.df.index[-1].strftime('%Y-%m-%d')

    def fit(self):
        if self.df is None:
            raise ValueError(
                'No data available. Please call load_data() before calling fit().')

        X, y = self.df[['Steers', 'Heifers', 'CPI', 'Cattle']], self.df['ClosingPrice']
        self.model.fit(X, y, shift=-self.shift)

        self.df['Prediction'] = self.model.predict(X)
        CalculateProbability(self.model, np.linspace(0.8, 1.2, 1001))

    def display(self, return_figures=False):
        if not self.fitted:
            self.fit()

        # prob distribution
        title = f"R2={self.model.R2:.2f} (as of {self.last_date})"
        fig1 = VisualizeProbability(
            self.model, self.current_price, 'Live cattle Price', title, False)

        # time series of predictions
        self.df = self.df.join(self.df.Prediction.shift(
            self.shift).rename('PredictedPrice'), how='outer')
        fig2 = px.line(self.df.ffill(), y=['PredictedPrice', 'ClosingPrice'])
        fig2.update_layout(xaxis_title='Time',
                           yaxis_title='Price', hovermode='x')
        if not return_figures:
            fig1.show(), fig2.show()
        else:
            return fig1, fig2

    def backtest(self, window):
        data = self.df[['Steers', 'Heifers', 'CPI', 'Cattle', 'ClosingPrice']].dropna().drop_duplicates()
        X, y = data[['Steers', 'Heifers', 'CPI', 'Cattle']], data.dropna()[
            'ClosingPrice']
        df_results = self.model.rolling_fit(
            X, y, shift=-self.shift, window=window)
        df_results['Observed'] = data.ClosingPrice
        # TODO: add PnL, convergence rate, etc.
        return df_results
