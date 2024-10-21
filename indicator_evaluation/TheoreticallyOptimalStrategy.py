import numpy as np
import datetime as dt
import pandas as pd
from util import get_data, plot_data


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "mfahad7"


def testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    """
    Theoretically Optimal Strategy
    :param symbol: Stock symbol
    :param sd: Start date
    :param ed: End date
    :param sv: Start value of the portfolio
    :return: DataFrame with trades
    """

    # Fetch adjusted close data
    stock_data = get_data([symbol], pd.date_range(sd, ed), colname="Adj Close").drop("SPY", axis=1)

    # Calculate daily returns
    daily_returns = stock_data.diff()

    # Buy if returns are positive, Sell if negative
    trade_signals = daily_returns.applymap(lambda x: "BUY" if x > 0 else "SELL" if x < 0 else 0).shift(-1)

    trades = pd.DataFrame(data=0, index=stock_data.index, columns=["Shares"])

    #trade data based on signal
    for i in range(trade_signals.shape[0]):
        if trade_signals.iloc[i, 0] == "BUY":
            trades.iloc[i, 0] = 1000
        elif trade_signals.iloc[i, 0] == "SELL":
            trades.iloc[i, 0] = -1000

        # Close next day
        if i + 1 < trade_signals.shape[0]:
            trades.iloc[i + 1, 0] -= trades.iloc[i, 0]

    return trades
