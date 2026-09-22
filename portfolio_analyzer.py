import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------------------------

TICKERS = ["AAPL", "MSFT", "GOOGL"]

WEIGHTS = [0.4, 0.3, 0.3]

START_DATE = "2021-01-01"

END_DATE = None

RISK_FREE_RATE = 0.03

TRADING_DAYS_PER_YEAR = 252


# ---------------------------------------------------------------------------
# 2. DOWNLOAD PRICE DATA
# ---------------------------------------------------------------------------

def fetch_price_data(tickers, start, end):
    """Download historical adjusted prices for a list of tickers."""

    print("Downloading market data...")

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        threads=False
    )["Close"]

    # If only one ticker is provided, yfinance returns a Series
    if isinstance(raw, pd.Series):
        raw = raw.to_frame(name=tickers[0])

    # Remove tickers that have no data
    raw = raw.dropna(axis=1, how="all")

    # Check that we actually received data
    if raw.empty:
        raise ValueError(
            "No market data was downloaded. "
            "Check your internet connection or yfinance."
        )

    # Check for tickers that failed to download
    missing_tickers = [
        ticker for ticker in tickers
        if ticker not in raw.columns
    ]

    if missing_tickers:
        print(
            f"Warning: Could not download data for: "
            f"{', '.join(missing_tickers)}"
        )

    print(f"Successfully downloaded data for: {', '.join(raw.columns)}")

    return raw


# ---------------------------------------------------------------------------
# 3. CALCULATE DAILY RETURNS
# ---------------------------------------------------------------------------

def compute_daily_returns(prices):
    """Calculate simple daily percentage returns."""

    if prices.empty:
        raise ValueError("Price data is empty.")

    return prices.pct_change().dropna()


# ---------------------------------------------------------------------------
# 4. CALCULATE PORTFOLIO RETURNS
# ---------------------------------------------------------------------------

def compute_portfolio_returns(daily_returns, weights):
    """Calculate portfolio daily returns using weighted asset returns."""

    # Make sure the number of weights matches the number of columns
    if len(weights) != len(daily_returns.columns):
        raise ValueError(
            "Number of weights does not match the number of "
            "available tickers."
        )

    weights = np.array(weights)

    return daily_returns.dot(weights)


# ---------------------------------------------------------------------------
# 5. ANNUALIZED RETURN
# ---------------------------------------------------------------------------

def annualize_return(
    daily_returns,
    periods=TRADING_DAYS_PER_YEAR
):
    """Compound daily returns into an annualized return."""

    if len(daily_returns) == 0:
        raise ValueError(
            "No daily return data available."
        )

    growth = (1 + daily_returns).prod()

    n_years = len(daily_returns) / periods

    if n_years <= 0:
        raise ValueError(
            "Not enough data to calculate annualized return."
        )

    return growth ** (1 / n_years) - 1


# ---------------------------------------------------------------------------
# 6. ANNUALIZED VOLATILITY
# ---------------------------------------------------------------------------

def annualize_volatility(
    daily_returns,
    periods=TRADING_DAYS_PER_YEAR
):
    """Scale daily standard deviation to annualized volatility."""

    if len(daily_returns) == 0:
        raise ValueError(
            "No daily return data available."
        )

    return daily_returns.std() * np.sqrt(periods)


# ---------------------------------------------------------------------------
# 7. SHARPE RATIO
# ---------------------------------------------------------------------------

def sharpe_ratio(
    ann_return,
    ann_vol,
    risk_free=RISK_FREE_RATE
):
    """Calculate risk-adjusted return using the Sharpe ratio."""

    if ann_vol == 0:
        return np.nan

    return (ann_return - risk_free) / ann_vol


# ---------------------------------------------------------------------------
# 8. CALCULATE DRAWDOWN
# ---------------------------------------------------------------------------

def compute_drawdown(daily_returns):
    """
    Calculate:
    - Wealth index
    - Running maximum
    - Drawdown from the running maximum
    """

    wealth_index = (1 + daily_returns).cumprod()

    running_max = wealth_index.cummax()

    drawdown = (
        (wealth_index - running_max)
        / running_max
    )

    return wealth_index, drawdown


# ---------------------------------------------------------------------------
# 9. MAXIMUM DRAWDOWN
# ---------------------------------------------------------------------------

def max_drawdown(drawdown):
    """Return the worst drawdown and the date it occurred."""

    if drawdown.empty:
        raise ValueError(
            "No drawdown data available."
        )

    return drawdown.min(), drawdown.idxmin()


# ---------------------------------------------------------------------------
# 10. PORTFOLIO SUMMARY
# ---------------------------------------------------------------------------

def summarize_portfolio(
    tickers,
    weights,
    port_returns
):
    """Calculate and display portfolio performance metrics."""

    wealth_index, drawdown = compute_drawdown(
        port_returns
    )

    ann_ret = annualize_return(
        port_returns
    )

    ann_vol = annualize_volatility(
        port_returns
    )

    sharpe = sharpe_ratio(
        ann_ret,
        ann_vol
    )

    mdd, mdd_date = max_drawdown(
        drawdown
    )

    print()
    print("=" * 55)
    print("PORTFOLIO SUMMARY")
    print("=" * 55)

    for ticker, weight in zip(tickers, weights):
        print(
            f"  {ticker:<8} weight: {weight:.1%}"
        )

    print("-" * 55)

    print(
        f"  Annualized Return:      {ann_ret:.2%}"
    )

    print(
        f"  Annualized Volatility:  {ann_vol:.2%}"
    )

    print(
        f"  Sharpe Ratio:           {sharpe:.2f}"
    )

    print(
        f"  Max Drawdown:           "
        f"{mdd:.2%}  (on {mdd_date.date()})"
    )

    print("=" * 55)

    return wealth_index, drawdown


# ---------------------------------------------------------------------------
# 11. PLOT RESULTS
# ---------------------------------------------------------------------------

def plot_results(
    wealth_index,
    drawdown,
    save_path="portfolio_performance.png"
):
    """Create and save portfolio growth and drawdown charts."""

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10, 8),
        sharex=True
    )

    # Portfolio growth
    axes[0].plot(
        wealth_index.index,
        wealth_index.values,
        color="#2563eb"
    )

    axes[0].set_title(
        "Portfolio Growth of $1"
    )

    axes[0].set_ylabel(
        "Wealth Index"
    )

    axes[0].grid(
        alpha=0.3
    )

    # Drawdown
    axes[1].fill_between(
        drawdown.index,
        drawdown.values,
        0,
        color="#dc2626",
        alpha=0.4
    )

    axes[1].set_title(
        "Portfolio Drawdown"
    )

    axes[1].set_ylabel(
        "Drawdown"
    )

    axes[1].grid(
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        save_path,
        dpi=150
    )

    print()
    print(
        f"Chart saved to: {save_path}"
    )

    plt.show()


# ---------------------------------------------------------------------------
# 12. MAIN PROGRAM
# ---------------------------------------------------------------------------

def main():

    # -------------------------------------------------------
    # Determine portfolio weights
    # -------------------------------------------------------

    if WEIGHTS is None:
        weights = [
            1 / len(TICKERS)
        ] * len(TICKERS)

    else:
        weights = WEIGHTS

    # -------------------------------------------------------
    # Validate weights
    # -------------------------------------------------------

    if len(weights) != len(TICKERS):
        raise ValueError(
            "Number of weights must match "
            "number of tickers."
        )

    if abs(sum(weights) - 1.0) > 1e-6:
        raise ValueError(
            "Weights must sum to 1.0"
        )

    # -------------------------------------------------------
    # Download prices
    # -------------------------------------------------------

    prices = fetch_price_data(
        TICKERS,
        START_DATE,
        END_DATE
    )

    # -------------------------------------------------------
    # Make sure all required tickers downloaded
    # -------------------------------------------------------

    missing_tickers = [
        ticker
        for ticker in TICKERS
        if ticker not in prices.columns
    ]

    if missing_tickers:
        raise ValueError(
            "The following tickers failed to download: "
            + ", ".join(missing_tickers)
            + ". Please try running the program again."
        )

    # -------------------------------------------------------
    # Calculate daily returns
    # -------------------------------------------------------

    daily_returns = compute_daily_returns(
        prices
    )

    # -------------------------------------------------------
    # Calculate portfolio returns
    # -------------------------------------------------------

    port_returns = compute_portfolio_returns(
        daily_returns,
        weights
    )

    # -------------------------------------------------------
    # Calculate portfolio metrics
    # -------------------------------------------------------

    wealth_index, drawdown = summarize_portfolio(
        TICKERS,
        weights,
        port_returns
    )

    # -------------------------------------------------------
    # Plot results
    # -------------------------------------------------------

    plot_results(
        wealth_index,
        drawdown
    )


# ---------------------------------------------------------------------------
# 13. RUN PROGRAM
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
