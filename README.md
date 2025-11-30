# Are we in an AI bubble?

Over the last few years, AI-related companies (especially chip designers and big tech) have delivered huge stock-market gains. This has led to constant claims that “we’re in an AI bubble” – and counter-claims that these moves are justified by fundamentals.

This project tries to **quantify** that debate using market data from Yahoo Finance.

The goal is not to *prove* or *disprove* a bubble (which is basically impossible in real time), but to ask a more concrete question:

> Do AI-related stocks behave in a way that is **consistent with bubble-like hype** compared to the rest of the market?

I focus on:

- an **equal-weight basket of AI-related stocks and ETFs**
- broad **benchmarks**: Nasdaq-100 (QQQ), S&P 500 (SPY), and a semiconductor ETF (SOXX)
- **risk and return metrics**: cumulative performance, volatility, rolling Sharpe ratios, drawdowns
- **dependencies** between AI names: return correlations and return distributions

Everything is implemented in a small Python package (`bubble/`) with functions for loading data, computing indicators and plotting results. The main analysis and interpretation live in a Jupyter notebook.

---

## 1. Data and Universe

All data come from **Yahoo Finance** via the [`yfinance`](https://pypi.org/project/yfinance/) library.

### AI-related tickers

The AI “basket” is a mix of individual stocks and AI-themed ETFs:

- **Large tech / platforms:** `MSFT`, `GOOGL`, `META`, `AMZN`
- **Semiconductors & hardware:** `NVDA`, `AMD`, `AVGO`, `ASML`, `TSM`
- **AI / robotics ETFs:** `BOTZ`, `ARKQ`, `AIQ`

### Benchmarks

- `QQQ` – Nasdaq-100 (growth / big tech)
- `SPY` – S&P 500 (broad US market)
- `SOXX` – Semiconductor ETF (sector benchmark)

The analysis uses **daily adjusted close prices** from **2020-01-01** to present day by default.

---

## 2. Methods & Functions

The core analysis is implemented in the `bubble` package.

### `bubble.loader`

- `load_stock_data(...)` – closing prices from Yahoo Finance for a list of tickers.

### `bubble.indicators`

- `calculate_returns(...)` – simple or log returns from price data.
- `calculate_index_returns(...)` – returns for a single index series.
- `build_equal_weight_index(...)` – constructs an equal-weight AI basket from individual prices.
- `calculate_rolling_volatility(...)` – rolling annualized volatility of returns.
- `calculate_rolling_correlation(...)` – rolling average correlation across AI names.
- `calculate_rolling_sharpe(...)` – rolling Sharpe ratio of the AI basket.
- `calculate_drawdown(...)` / `calculate_max_drawdown(...)` – drawdown series and worst drawdown.

### `bubble.visualizations`

All plotting uses `matplotlib`/`seaborn` behind the scenes:

- `plot_normalized_prices(...)` – normalised price paths for individual AI names.
- `plot_index_vs_benchmark(...)` – AI basket vs QQQ/SPY/SOXX.
- `plot_correlation_matrix(...)` – correlation heatmap of AI stock returns.
- `plot_rolling_correlation(...)` – time-varying average correlation.
- `plot_rolling_volatility(...)` – rolling volatility (optionally for a subset of tickers).
- `plot_rolling_sharpe(...)` – rolling Sharpe of the AI basket.
- `plot_drawdown(...)` – drawdown (underwater) charts.
- `plot_return_distribution(...)` – return distribution comparison.

### Notebook

The main analysis lives in:

- `presentation/ai_bubble_analysis.ipynb`

This notebook:

1. Loads AI and benchmark data from Yahoo Finance.
2. Builds an equal-weight AI index and benchmark indices.
3. Computes returns, rolling volatility, rolling correlations and rolling Sharpe ratios.
4. Analyzes drawdowns for the AI basket and benchmarks.
5. Compares return distributions of the AI basket vs QQQ / SPY / SOXX.
6. Interprets all figures in the context of “AI bubble / AI hype”.

---

## 3. Project Structure

```
ai-bubble/
├── bubble/                        
│   ├── __init__.py
│   ├── loader.py                  
│   ├── indicators.py              
│   └── visualizations.py          
├── presentation/
│   └── ai_bubble_analysis.ipynb
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 4. Installation
1. Clone the repository and get into it:

```bash
git clone https://github.com/akbargafurov/ai-bubble.git
cd ai-bubble
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# on Mac/Linux
source venv/bin/activate
# on Windows
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

The key Python libraries used are:
* pandas for data manipulation
* numpy for numerical calculations
* matplotlib and seaborn for visualisation
* yfinance for downloading market data

---

## 5. Running the analysis

From the project root:
```bash
jupyter lab
# or 
jupyter notebook
```

Then open:
```bash
presentation/ai_bubble_analysis.ipynb
```

and run all cells (Kernel → “Restart & Run All”).

The notebook will:
* Load AI and benchmark price data.
* Build the equal-weight AI basket and benchmark indices.
* Produce plots of performance, volatility, drawdowns and correlations.
* Compare return distributions of the AI basket vs QQQ/SPY/SOXX.
* Provide textual commentary interpreting each figure in the context of “AI hype / bubble”.

---

## 6. Key findings
* The equal-weight AI basket has massively outperformed broad benchmarks (QQQ, SPY, SOXX) since 2020.
* This outperformance comes with higher volatility, deeper drawdowns and a fatter-tailed return distribution than the benchmarks.
* AI-related stocks often move together, with elevated return correlations, especially during periods of stress or hype, suggesting they are traded as a single thematic “AI trade”.
* Rolling volatility for representative names (e.g. NVDA, MSFT, GOOGL, META) spikes around the COVID crash, the 2022 tech selloff and the 2023–2024 AI rally, confirming that these are high-beta, high-risk stocks.

Taken together, the evidence points to strong AI hype and concentrated optimism in a subset of AI-related stocks. Price behavior, risk characteristics and correlations all look consistent with a speculative phase in AI assets.

At the same time, some of the gains may be justified by genuine structural change and earnings growth, so it would be too strong to declare a clear, universal bubble.

The most honest statement is:

> We are likely seeing a powerful hype cycle, with bubble-like behavior in some flagship AI names, rather than a uniform bubble across everything related to AI.

---

## 7. Limitations

There are some limitations present in this project. In the future, they can be addressed to support a broader analysis of the financial situation around AI-related companies. For now, these limitations are as follows:
* The analysis is based on daily prices and a limited time window (from 2020), so it may miss longer-term cycles.
* Fundamental data (earnings, cash flows, detailed valuation models) are not modeled explicitly; the project focuses on market behavior, not intrinsic value.
* The project is descriptive and educational only; it is neither a trading strategy nor does it constitute investment advice.
