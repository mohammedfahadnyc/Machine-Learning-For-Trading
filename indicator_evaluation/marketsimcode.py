import pandas as pd
from util import get_data


def author():
    return 'mfahad7'  # Replace with your GT username


def study_group():
    """
    Returns
        A comma-separated string of GT_Name of each member of your study group
    Return type
        str
    """
    return "mfahad7"


def compute_portvals(
        trades,
        start_val=100000,
        commission=0.0,
        impact=0.0
):
    """
    Simulates the portfolio values over time, given a set of trades DataFrame.

    :param trades: DataFrame with trades (BUY/SELL). Index: Date, Column: Symbol
    :param start_val: Initial cash value in the portfolio.
    :param commission: The fixed commission cost per trade.
    :param impact: The market impact factor affecting prices when trading.
    :return: DataFrame with the portfolio values indexed by date.
    :rtype: pandas.DataFrame
    """

    # Define the date range based on the trades
    start_date = trades.index.min()
    end_date = trades.index.max()

    # Get the list of symbols from trades
    symbols = trades.columns

    # Fetch price data for the symbols
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices['Cash'] = 1.0  # Add a cash column for cash tracking

    # Initialize the trades and holdings DataFrames
    holdings = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    holdings['Cash'].iloc[0] = start_val

    for date, trade in trades.iterrows():
        for symbol in symbols:
            shares = trade[symbol]
            if shares != 0:
                price = prices.loc[date, symbol]
                trade_value = shares * price
                trade_cost = trade_value * impact + commission

                # Update holdings based on trades
                holdings.loc[date, symbol] += shares
                holdings.loc[date, 'Cash'] -= trade_value + trade_cost

    # Calculate the portfolio values over time
    portfolio_values = (holdings * prices).sum(axis=1)

    return pd.DataFrame(portfolio_values, columns=['Portfolio Value'])


def test_code():
    """
    Helper function to test the compute_portvals function.
    """
    # Example trades DataFrame
    dates = pd.date_range('2008-01-01', '2009-12-31')
    trades = pd.DataFrame(0, index=dates, columns=['JPM'])
    trades.loc['2008-01-10'] = 1000  # Buy 1000 shares
    trades.loc['2008-01-11'] = -1000  # Sell 1000 shares

    portvals = compute_portvals(trades, start_val=100000)

    if isinstance(portvals, pd.DataFrame):
        print(portvals.head())
    else:
        print("Error: compute_portvals should return a DataFrame")


if __name__ == "__main__":
    test_code()
