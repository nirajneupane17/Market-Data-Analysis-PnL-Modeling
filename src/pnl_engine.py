"""
pnl_engine.py
=============
PnL calculation, attribution, and trade analytics engine.

Author : Niraj Neupane | github.com/nirajneupane17
Project: Market Data Analysis & PnL Modeling (Project 9 / 10)
"""
import numpy as np
import pandas as pd
from typing import List, Dict
import warnings; warnings.filterwarnings("ignore")


def compute_portfolio_pnl(returns: pd.DataFrame, weights: np.ndarray,
                            notional: float = 1_000_000) -> pd.DataFrame:
    port_ret = (returns * weights).sum(axis=1)
    pnl = port_ret * notional
    df = pd.DataFrame({'portfolio_return': port_ret, 'portfolio_pnl': pnl,
                        'cumulative_pnl': pnl.cumsum()}, index=returns.index)
    for i, col in enumerate(returns.columns):
        df[f'{col}_contrib'] = returns[col] * weights[i] * notional
    return df

def pnl_attribution(pnl_df: pd.DataFrame, assets: List[str]) -> Dict:
    contrib_cols = [f'{a}_contrib' for a in assets]
    total = pnl_df[contrib_cols].sum()
    pct   = (abs(total) / abs(total).sum() * 100).round(2)
    return {'total_contrib_usd': total.round(2),
            'contrib_pct':       pct,
            'total_pnl':         pnl_df['portfolio_pnl'].sum().round(2),
            'cumulative_pnl':    pnl_df['cumulative_pnl'].iloc[-1].round(2)}

def annual_pnl(pnl_df: pd.DataFrame) -> pd.DataFrame:
    return (pnl_df['portfolio_pnl'].resample('YE').sum()
            .to_frame('annual_pnl').assign(
                cumulative=lambda x: x['annual_pnl'].cumsum()))

def monthly_pnl(pnl_df: pd.DataFrame) -> pd.Series:
    return pnl_df['portfolio_pnl'].resample('ME').sum()

def trade_analytics(blotter: pd.DataFrame) -> Dict:
    pnl = blotter['pnl']
    wins = pnl > 0
    return {
        'total_trades':   len(blotter),
        'win_rate':        round(wins.mean() * 100, 2),
        'avg_pnl':         round(pnl.mean(), 2),
        'avg_win':         round(pnl[wins].mean(), 2),
        'avg_loss':        round(pnl[~wins].mean(), 2),
        'profit_factor':   round(abs(pnl[wins].sum() / pnl[~wins].sum()), 3),
        'total_pnl':       round(pnl.sum(), 2),
        'max_win':         round(pnl.max(), 2),
        'max_loss':        round(pnl.min(), 2),
        'win_rate_long':   round((blotter[blotter['direction']==1]['pnl']>0).mean()*100, 2),
        'win_rate_short':  round((blotter[blotter['direction']==-1]['pnl']>0).mean()*100, 2),
    }

def win_rate_by_asset(blotter: pd.DataFrame) -> pd.Series:
    return blotter.groupby('asset').apply(
        lambda x: round((x['pnl']>0).mean()*100, 2))

if __name__ == "__main__":
    print("pnl_engine.py OK")
