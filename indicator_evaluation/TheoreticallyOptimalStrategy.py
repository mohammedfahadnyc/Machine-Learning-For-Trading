import pandas as pd
import datetime as dt
from util import get_data

def author():
    return 'mfahad7'  # Replace with your GT username

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    """
    Implements the Theoretically Optimal Strategy (TOS), which returns the trades DataFrame.

    Parameters:
        symbol - The stock symbol to act on
        sd     - A DateTime object that represents the start date
        ed     - A DateTime object that represents the end date
        sv     - Start value of the portfolio

    Returns:
        trades - A single column DataFrame, indexed by date, representing trades per day.
                 Legal values are +1000 (BUY), -1000 (SELL), and 0.0 (HOLD).
    """
    # Fetch price data for the given symbol in the specified date range
    dates = pd.date_range(sd, ed)
    prices = get_data([symbol], dates)
    prices = prices[symbol]  # Only keep the symbol's price data

    # Initialize the trades DataFrame
    trades = pd.DataFrame(0.0, index=prices.index, columns=[symbol])

    # Loop over prices and generate trades based on perfect foresight
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            trades.iloc[i] = 1000  # BUY
        elif prices[i] < prices[i - 1]:
            trades.iloc[i] = -1000  # SELL
        # If the price stays the same, do nothing (0 by default)

    return trades

if __name__ == "__main__":
    # Example usage
    df_trades = testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    print(df_trades.head())  # Print the first few trades to verify
