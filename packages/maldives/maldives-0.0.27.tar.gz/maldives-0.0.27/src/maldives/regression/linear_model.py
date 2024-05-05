import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import HuberRegressor
from sklearn.metrics import r2_score

from maldives.backtest.utils import CalculateProbability,  VisualizeProbability


def _shift_data(X, y, n):
    # +ve: features predict previous value, -ve: features predict next value
    if n == 0:
        return X, y
    return (X[n:], y[:-n]) if n > 0 else (X[:n], y[-n:])


def _add_lagged_y_to_x(X, y, n):
    # TODO add lagged response to feature, n is (list of) lag
    pass

class LinearRegressor(object):
    def __init__(self, fitter=HuberRegressor(), transform=None, invtransform=None):
        """Basic linear regression model

        Args:
            fitter (scikit-learn model, optional): Model object with fit(), predict() and score(). Defaults to HuberRegressor().
            transform (Function, optional): Transformation applied to data, e.g. log. Defaults to None.
            invtransform (Function, optional): Function to invert transform, e.g. exp. Defaults to None.
        """
        self.fitter = fitter
        identity = (lambda x: x)
        self.transform = identity if transform is None else transform
        self.invtransform = identity if invtransform is None else invtransform
        self.prediction = None
        self.observed = None
        self.R2 = 0
        self.shift = 0

    def _preprocess(self, X, y):
        X_shifted, y_shifted = _shift_data(X, y, self.shift)
        self.observed = y_shifted
        self.X_transformed = self.transform(X_shifted)
        self.y_transformed = self.transform(y_shifted)

    def fit(self, X, y, shift=0, **kwargs):
        """Fit linear model to data

        Args:
            X (array): features
            y (array): response
            shift (int, optional): shift in y. Positive means current features are used to predict previous response. 
            Negative means current features are used to predict next response. Defaults to 0.
        """
        self.shift = shift
        self._preprocess(X, y)
        self.fitter.fit(self.X_transformed, self.y_transformed, **kwargs)
        self.ypred = self.invtransform(self.fitter.predict(self.X_transformed))
        self.R2 = r2_score(self.observed, self.ypred)

    def rolling_fit(self, X, y, shift=0, window=1, **kwargs):
        """Run a rolling fit prediction over the dataset

        Args:
            X (array): features
            y (array): response
            shift (int, optional): shift in y. Positive means current features are used to predict previous response. 
            Negative means current features are used to predict next response. Defaults to 0.
            window (int, optional): Size of the rolling window. Defaults to 1.
        """
        self.shift = shift
        self._preprocess(X, y)

        # loop over windows
        ypred = []
        R2 = []
        coeffs = []
        ind = []
        for start_ind in range(len(self.y_transformed)-window):
            Xw = self.X_transformed[start_ind:start_ind+window]
            yw = self.y_transformed[start_ind:start_ind+window]
            self.fitter.fit(Xw, yw, **kwargs)
            ypredw = self.invtransform(self.fitter.predict(Xw))
            ypred.append(ypredw[-1])
            R2.append(r2_score(self.invtransform(yw), ypredw))
            coeffs.append(self.fitter.coef_)
            if hasattr(Xw, 'index'):
                ind.append(Xw.index[-1])

        results = pd.DataFrame(coeffs)
        results['Prediction'] = ypred
        results['R2'] = R2
        if len(ind) > 0:
            results.index = ind
        return results

    def predict(self, X, **kwargs):
        """Predict on feature.

        Args:
            X (array): features

        Returns:
            prediction (array): predicted response
        """
        self.prediction = self.invtransform(
            self.fitter.predict(self.transform(X), **kwargs))
        return self.prediction


class RegressionModel(object):

    def __init__(self, df, features, target, shift=30):
        """Interface for regression model.

        Args:
            df (pd.Dataframe): pandas dataframe containing the dataset
            features (list of str): column names for features
            target (str): column name for target
            shift (int, optional): day shift for regression. Defaults to 30.
        """
        self.df = df
        self.features = features
        self.target = target
        self.fitted = False

        self.model = LinearRegressor(transform=np.log, invtransform=np.exp)
        self.last_date = df.index[-1].strftime('%Y-%m-%d')
        self.current_price = df[target].values[-1]
        self.shift = shift

    def fit(self, prange=np.linspace(0.8, 1.2, 1001)):
        if self.df is None:
            raise ValueError(
                'No data available.')

        X, y = self.df[self.features], self.df[self.target]
        self.model.fit(X, y, shift=-self.shift)

        self.df['Prediction'] = self.model.predict(X)
        CalculateProbability(self.model, prange)

    def display(self, return_figures=False, xlabel='Price'):
        if not self.fitted:
            self.fit()

        # prob distribution
        title = f"R2={self.model.R2:.2f} (as of {self.last_date})"
        fig1 = VisualizeProbability(
            self.model, self.current_price, xlabel, title, False)

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
        X, y = self.df[self.features], self.df[self.target]
        df_results = self.model.rolling_fit(
            X, y, shift=-self.shift, window=window)
        df_results['Observed'] = y
        # TODO: add PnL, convergence rate, etc.
        return df_results
