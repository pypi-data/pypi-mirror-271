import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde


def CalculateUncertainty(model, use_percentage=True):
    if (not hasattr(model, 'ypred')) or (not hasattr(model, 'observed')):
        raise ValueError(
            'Model must contain "observed" values and "ypred" values.')
    if model.prediction is None or model.observed is None:
        raise ValueError('Model is not fitted.')

    if use_percentage:
        model.uncertainty = gaussian_kde(model.observed/model.ypred)
    else:
        model.uncertainty = gaussian_kde(model.observed - model.ypred)

    return model.uncertainty


def CalculateProbability(model, prange,  current_pred=None, use_percentage=True):
    if (not hasattr(model, 'uncertainty')) or (model.uncertainty is None):
        CalculateUncertainty(model, use_percentage)
    if current_pred is None:
        current_pred = model.prediction[-1]

    values = (prange*current_pred) if use_percentage else (prange+current_pred)

    model.prob = pd.DataFrame(model.uncertainty(
        prange), index=values, columns=['probability'])
    model.prob['pvalue'] = [
        model.uncertainty.integrate_box_1d(p, np.inf) for p in prange]
    model.prob = model.prob.round(4)

    return model.prob


def VisualizeProbability(model, current_value=None, xlabel='Value', title='', show_figure=False):
    if (not hasattr(model, 'prob')) or (model.prob is None):
        raise ValueError(
            'Probabilities has not been calculated for model. Call CalculateProbability(model) first.')

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig1 = px.line(model.prob, y='pvalue')
    fig2 = px.line(model.prob, y='probability')
    fig2.update_traces(yaxis="y2")
    fig.add_traces(fig1.data + fig2.data)
    fig.add_vline(current_value, line_color='red',
                   annotation_text='Current Value')
    fig.layout.xaxis.title = xlabel
    fig.layout.yaxis.title = "p-value"
    fig.layout.yaxis2.title = "Probability"
    fig.update_layout(title=title, hovermode='x')
    fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    if show_figure:
        fig.show()
    return fig
        
def ConvergenceTrades(data, observed_column='Observed', pred_column='Prediction'):
# FIXME: add percentage_based

    df = data[[observed_column,pred_column,'R2']].dropna()
    df.loc[:,'Difference'] = df.eval(f'{pred_column}-{observed_column}')

    df_underprice = df.query('Difference >= 0')
    df_underprice.loc[:,'Time'] = df_underprice.index
    df_overprice = df.query('Difference < 0')
    df_overprice.loc[:,'Time'] = df_overprice.index

    df_short = pd.merge_asof(df_overprice, df_underprice, left_index=True, right_index=True, suffixes=('1','2'), direction='forward')
    df_long = pd.merge_asof(df_underprice, df_overprice, left_index=True, right_index=True, suffixes=('1','2'), direction='forward')

    df_short.loc[:,'Side'] = -1
    df_long.loc[:,'Side'] = +1

    df_trades = pd.concat([df_short,df_long]).sort_index().dropna()
    df_trades.loc[:,'PnL'] = df_trades.eval(f'Side*({observed_column}2-{observed_column}1)')
    df_trades.loc[:,'Days'] = (df_trades['Time2']-df_trades['Time1']).dt.days
    df_trades.loc[:,'Speed'] = df_trades.eval('PnL/Days')
    df_trades.loc[:,'AbsDifference'] = df_trades.eval('abs(Difference1)')

    return df_trades