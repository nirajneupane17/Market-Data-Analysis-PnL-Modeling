# Market Data Analysis & PnL Modeling

End-to-end market data analysis pipeline — daily PnL calculation,
asset-level attribution, risk-adjusted performance metrics, trade
analytics across 500 trades, and factor decomposition (alpha/beta)
vs SPY benchmark. USD 1M portfolio across SPY, QQQ, TLT, GLD, HYG.

![Market PnL Bloomberg](results/market_pnl_bloomberg.gif)

---

## Key Results

| Metric | Value |
|---|---|
| Portfolio Sharpe Ratio | 0.12 |
| Sortino Ratio | 0.17 |
| Calmar Ratio | 0.01 |
| Maximum Drawdown | -37.2% |
| Ann. Volatility | 13.6% |
| Beta vs SPY | 0.84 |
| Win Rate (500 trades) | 50.4% |
| Total Cumulative PnL | USD 84K |

---

## Project Structure

```
Market-Data-Analysis-PnL-Modeling/
├── data/
│   ├── market_prices.csv       # 5-asset daily prices 2020-2024 (1,305 obs)
│   ├── market_returns.csv      # Daily returns
│   └── trade_blotter.csv       # 500 trades with entry/exit/PnL
├── notebooks/
│   ├── 01_market_data_analysis.ipynb
│   ├── 02_pnl_analysis.ipynb
│   ├── 03_pnl_attribution.ipynb
│   ├── 04_risk_metrics.ipynb
│   └── 05_factor_decomposition.ipynb
├── src/
│   ├── market_data.py          # Data loading, rolling metrics, risk-return
│   ├── pnl_engine.py           # PnL calculation, attribution, trade analytics
│   └── factor_analysis.py      # Beta, alpha, rolling correlations
├── results/
│   ├── 01_market_performance.png
│   ├── 02_pnl_analysis.png
│   ├── 03_pnl_attribution.png
│   ├── 04_risk_metrics.png
│   ├── 05_trade_analytics.png
│   ├── 06_factor_decomposition.png
│   ├── 07_summary_dashboard.png
│   ├── market_pnl_bloomberg.gif
│   └── market_pnl_video.mp4
└── README.md
```

---

## Author

**Niraj Neupane** — Quantitative Risk Analyst · BlackRock
GitHub: [github.com/nirajneupane17](https://github.com/nirajneupane17)

Project 9 of 10 in the Quant Risk GitHub Series.
