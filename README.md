Portfolio Analyzer

A Python tool that pulls real market data and computes portfolio-level performance and risk metrics in seconds. Designed to bridge the gap between textbook portfolio theory and practical financial analysis.

Project Overview

Portfolio Analyzer downloads historical price data via yfinance, calculates weighted portfolio returns, and computes key financial metrics:

Annualized Return — compound daily returns into a single annual figure
Annualized Volatility — scale daily standard deviation up to risk per year
Sharpe Ratio — excess return per unit of risk (return vs. risk-free rate)
Maximum Drawdown — worst peak-to-trough loss and when it occurred

The tool produces a clean 2-panel chart showing portfolio growth over time and drawdown periods, saving it as a PNG.

Why I Built This

I'm a Year 2 Business & Financial Technology student at Nanyang Polytechnic, focused on fintech and self-directed investing. I was working through my self-study curriculum (Book 07: The Finance Track, which covers risk metrics, portfolio construction, and backtesting) and realized I was learning these concepts in isolation — annualized returns, Sharpe ratios, drawdowns — but not actually applying them to real portfolios.

This project is my way of connecting the dots:

Theory → Practice: Taking concepts from my coursework (risk/return decomposition, volatility annualization, wealth indexing via cumprod) and building something I can run on any portfolio
Real Data: Using live market data instead of hypothetical examples
Reusable Tool: Something I can modify and reuse as I learn more about portfolio construction and risk management
What I Learned
Technical Skills
Data Pipelines: Download, clean, and align price data for multiple assets using yfinance and pandas
Financial Calculations:
Converting daily returns into annualized figures (compounding and scaling)
Computing portfolio returns as a weighted average of individual ticker returns
Calculating wealth index (growth of $1) via cumprod() — the foundation of drawdown analysis
Identifying drawdown as (wealth - running_max) / running_max using cummax()
Risk-adjusted return metrics (Sharpe ratio: excess return per unit of volatility)
Data Visualization: Multi-panel plotting with matplotlib to show both growth and drawdown side-by-side
Software Engineering: Modular functions, configuration at the top of the file, error handling for mismatched weights
Finance Concepts (Reinforced)
Annualization: Why and how daily volatility scales by √252 (trading days per year) — not just a formula, but why it matters
Wealth Indexing: How (1 + returns).cumprod() grows $1 into a full portfolio trajectory
Drawdown Analysis: Peak-to-trough losses tell a different story than volatility alone — they capture the severity of losses
Portfolio Theory Basics: How weights combine individual asset risks and returns into a portfolio outcome
Risk-Free Rate: Why the Sharpe ratio subtracts the risk-free rate — it's the excess return for taking risk
Getting Started
Prerequisites
Python 3.8+
pip (package manager)
Installation & Setup
Clone the repository
bash
   git clone https://github.com/<your-username>/portfolio-analyzer.git
   cd portfolio-analyzer
Create a virtual environment (recommended)
bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies
bash
   pip install -r requirements.txt
Edit the configuration (optional) Open portfolio_analyzer.py and scroll to the Configuration section:
python
   TICKERS = ["AAPL", "MSFT", "GOOGL"]   # Your portfolio tickers
   WEIGHTS = [0.4, 0.3, 0.3]             # Your allocations (must sum to 1.0)
   START_DATE = "2021-01-01"
   END_DATE = None                       # None = up to today
   RISK_FREE_RATE = 0.03                 # Annualized risk-free rate
Run the analyzer
bash
   python portfolio_analyzer.py
Example Output
==================================================
PORTFOLIO SUMMARY
==================================================
  AAPL     weight: 40.0%
  MSFT     weight: 30.0%
  GOOGL    weight: 30.0%
--------------------------------------------------
  Annualized Return:      22.09%
  Annualized Volatility:  16.03%
  Sharpe Ratio:           1.19
  Max Drawdown:           -20.89%  (on 2023-04-10)
==================================================

Chart saved to portfolio_performance.png

A chart (portfolio_performance.png) is saved showing:

Top panel: Wealth index (portfolio growth of $1)
Bottom panel: Drawdown over time (peak-to-trough losses highlighted in red)
Project Structure
portfolio-analyzer/
├── portfolio_analyzer.py      # Main script (config + all functions)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── example_output.png         # Sample chart output
How It Works (Under the Hood)
1. Data Fetching
python
prices = yf.download(["AAPL", "MSFT"], start="2021-01-01")["Close"]

Downloads adjusted close prices for all tickers into a DataFrame.

2. Daily Returns
python
daily_returns = prices.pct_change().dropna()

Converts prices into % changes day-over-day.

3. Portfolio Returns (Weighted)
python
portfolio_returns = daily_returns.dot(weights)  # Dot product = weighted sum

Combines individual returns using your allocation weights.

4. Annualization
python
ann_return = (1 + daily_returns).prod() ** (1/n_years) - 1
ann_volatility = daily_returns.std() * np.sqrt(252)

Scales daily metrics up to annual figures.

5. Drawdown
python
wealth_index = (1 + daily_returns).cumprod()
running_max = wealth_index.cummax()
drawdown = (wealth_index - running_max) / running_max

Tracks peak-to-trough losses over time.

6. Visualization

matplotlib creates a 2-panel chart with growth and drawdown.

Next Steps & Improvements
 Add correlation matrix between tickers (to understand diversification benefit)
 Add rolling Sharpe ratio (to see if strategy improves/degrades over time)
 Accept portfolio weights from a CSV file instead of hardcoding
 Add sector/industry breakdowns
 Compute beta and compare to a benchmark (e.g., SPY, S&P 500)
 Output a summary report to PDF or Excel
Why This Matters for My Career



This project is for educational purposes. Feel free to fork, modify, and use for your own portfolio analysis.

Contact

Ryan Lim Rui Yang
Nanyang Polytechnic | Business & Financial Technology
Interested in fintech, self-directed investing, and portfolio construction.
LinkedIn | GitHub

Last Updated: September 2026
Status: Active | Regularly refined as I progress through my coursework
