"""
market_data.py
==============
Market data loading, cleaning, and feature engineering
for the Market Data Analysis & PnL Modeling project.

Author : Niraj Neupane | github.com/nirajneupane17
Project: Market Data Analysis & PnL Modeling (Project 9 / 10)
"""
import numpy as np
import pandas as pd
from typing import List, Optional, Dict
import warnings; warnings.filterwarnings("ignore")


def load_prices(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col='Date', parse_dates=True)

def load_returns(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col='Date', parse_dates=True)

def compute_returns(prices: pd.DataFrame, method: str = 'simple') -> pd.DataFrame:
    if method == 'log':
        return np.log(prices / prices.shift(1)).dropna()
    return prices.pct_change().dropna()

def normalise_prices(prices: pd.DataFrame, base: float = 100.0) -> pd.DataFrame:
    return prices / prices.iloc[0] * base

def rolling_metrics(returns: pd.Series, window: int = 63) -> pd.DataFrame:
    scale = np.sqrt(252)
    df = pd.DataFrame(index=returns.index)
    df['rolling_vol']    = returns.rolling(window).std() * scale * 100
    df['rolling_return'] = returns.rolling(window).mean() * 252 * 100
    df['rolling_sharpe'] = (returns.rolling(window).mean() /
                             returns.rolling(window).std() * scale)
    df['rolling_skew']   = returns.rolling(window).skew()
    df['rolling_kurt']   = returns.rolling(window).kurt()
    return df.dropna()

def compute_drawdown(returns: pd.Series) -> pd.Series:
    cum = (1 + returns).cumprod()
    return cum / cum.cummax() - 1

def risk_return_summary(returns: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in returns.columns:
        r = returns[col].dropna()
        dd = compute_drawdown(r)
        sharpe = r.mean() / r.std() * np.sqrt(252)
        sortino = r.mean() / r[r<0].std() * np.sqrt(252)
        rows.append({'asset': col,
            'ann_return_pct': round(r.mean()*252*100, 2),
            'ann_vol_pct':    round(r.std()*np.sqrt(252)*100, 2),
            'sharpe':         round(sharpe, 3),
            'sortino':        round(sortino, 3),
            'max_dd_pct':     round(dd.min()*100, 2),
            'skewness':       round(r.skew(), 3),
            'kurtosis':       round(r.kurt(), 3)})
    return pd.DataFrame(rows).set_index('asset')

if __name__ == "__main__":
    import numpy as np
    dates = pd.date_range('2020-01-01', periods=500, freq='B')
    ret = pd.Series(np.random.normal(0, 0.01, 500), index=dates)
    print(rolling_metrics(ret).tail(3))
    print("market_data.py OK")
