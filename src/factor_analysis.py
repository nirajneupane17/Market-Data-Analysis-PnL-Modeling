"""
factor_analysis.py
==================
Factor decomposition: beta, alpha, rolling correlations,
and regime analysis for portfolio returns.

Author : Niraj Neupane | github.com/nirajneupane17
Project: Market Data Analysis & PnL Modeling (Project 9 / 10)
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import Dict, List
import warnings; warnings.filterwarnings("ignore")


def compute_beta_alpha(port_ret: pd.Series, bench_ret: pd.Series) -> Dict:
    common = port_ret.index.intersection(bench_ret.index)
    X = bench_ret.loc[common].values.reshape(-1, 1)
    y = port_ret.loc[common].values
    lr = LinearRegression(); lr.fit(X, y)
    resid = y - lr.predict(X)
    return {'beta':   round(lr.coef_[0], 4),
            'alpha':  round(lr.intercept_ * 252 * 100, 4),
            'r2':     round(lr.score(X, y), 4),
            'te':     round(resid.std() * np.sqrt(252) * 100, 4),
            'ir':     round((resid.mean() * 252) / (resid.std() * np.sqrt(252)), 4)}

def rolling_beta(port_ret: pd.Series, bench_ret: pd.Series,
                  window: int = 63) -> pd.Series:
    betas = []
    for i in range(window, len(port_ret)):
        p = port_ret.iloc[i-window:i].values
        b = bench_ret.iloc[i-window:i].values
        if len(b) == window:
            lr = LinearRegression()
            lr.fit(b.reshape(-1,1), p)
            betas.append(lr.coef_[0])
        else:
            betas.append(np.nan)
    return pd.Series(betas, index=port_ret.index[window:], name='rolling_beta')

def rolling_correlations(port_ret: pd.Series, factor_rets: pd.DataFrame,
                          window: int = 63) -> pd.DataFrame:
    df = pd.DataFrame(index=port_ret.index)
    for col in factor_rets.columns:
        df[f'corr_{col}'] = port_ret.rolling(window).corr(factor_rets[col])
    return df.dropna()

def annual_factor_decomp(port_ret: pd.Series, bench_ret: pd.Series) -> pd.DataFrame:
    rows = []
    for yr in port_ret.index.year.unique():
        p = port_ret.loc[str(yr)]; b = bench_ret.loc[str(yr)]
        if len(p) > 20:
            res = compute_beta_alpha(p, b)
            res['year'] = yr; rows.append(res)
    return pd.DataFrame(rows).set_index('year')

if __name__ == "__main__":
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=500, freq='B')
    p = pd.Series(np.random.normal(0.0004, 0.01, 500), index=dates)
    b = pd.Series(np.random.normal(0.0004, 0.012, 500), index=dates)
    print(compute_beta_alpha(p, b))
    print("factor_analysis.py OK")
