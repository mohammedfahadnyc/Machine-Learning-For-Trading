import pandas as pd
from util import get_data


def author():
    return 'mfahad7'


def compute_portvals(orders, start_date, end_date, start_val=100000, commission=0.0, impact=0.0):
    """
    Simulates market portfolio and returns the portfolio values.
    :param orders: DataFrame of orders
    :param start_date: Start date
    :param end_date: End date
    :param start_val: Starting portfolio value
    :param commission: Fixed commission per trade
    :param impact: Impact of trades on stock prices
    :return: DataFrame with portfolio values
    """


    unique_symbols = orders["Symbol"].unique()
    price_data = get_data(unique_symbols, pd.date_range(start_date, end_date)).drop("SPY", axis=1)
    price_data["Cash"] = 1.0

    #trades and holdings
    trades = pd.DataFrame(data=0.0, index=price_data.index, columns=price_data.columns)

    for i in range(orders.shape[0]):
        order_date = orders.index[i]
        symbol = orders.iloc[i]["Symbol"]
        shares = orders.iloc[i]["Shares"]
        order_type = orders.iloc[i]["Order"]

        trade_multiplier = 1 if order_type == "BUY" else -1
        trades.at[order_date, symbol] += trade_multiplier * shares
        cash_impact = -trade_multiplier * price_data.at[order_date, symbol] * shares
        trades.at[order_date, "Cash"] += cash_impact - commission - abs(cash_impact) * impact

    #holdings and portfolio values
    holdings = trades.cumsum()
    holdings["Cash"] += start_val
    portfolio_values = (holdings * price_data).sum(axis=1)

    return portfolio_values


def test_code():
    """
    Helper function to test the code implementation
    """
    orders_file = "./orders/orders-01.csv"
    start_val = 1000000

    port_vals = compute_portvals(orders=orders_file, start_date="2008-01-01", end_date="2009-12-31",
                                 start_val=start_val)
    if isinstance(port_vals, pd.DataFrame):
        port_vals = port_vals[port_vals.columns[0]]
    else:
        print("Warning: The function did not return a DataFrame")
