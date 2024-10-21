import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from util import get_data
from indicators import calculate_golden_cross, calculate_ema, compute_rsi, calculate_money_flow, compute_macd, \
    generate_plot, generate_split_plot
import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals

def author():
    return "mfahad7"

if __name__ == "__main__":

    start_date = dt.date(2008, 1, 1)
    end_date = dt.date(2009, 12, 31)
    stock_symbols = ["JPM"]

    # stock data
    high_prices = get_data(stock_symbols, pd.date_range(start_date, end_date), colname="High").drop("SPY", axis=1)
    low_prices = get_data(stock_symbols, pd.date_range(start_date, end_date), colname="Low").drop("SPY", axis=1)
    volumes = get_data(stock_symbols, pd.date_range(start_date, end_date), colname="Volume").drop("SPY", axis=1)
    adj_closes = get_data(stock_symbols, pd.date_range(start_date, end_date), colname="Adj Close").drop("SPY", axis=1)

    # indicators
    golden_cross = calculate_golden_cross(adj_closes)
    generate_plot(golden_cross, "Golden Cross")

    ema_values = calculate_ema(adj_closes, 30)
    generate_plot(ema_values, "Exponential Moving Average")

    rsi_values = compute_rsi(adj_closes)
    generate_split_plot(rsi_values, "RSI Indicator")

    money_flow_values = calculate_money_flow(adj_closes, low_prices, high_prices, volumes)
    generate_split_plot(money_flow_values, "Money Flow Index")

    macd_values = compute_macd(adj_closes)
    generate_split_plot(macd_values, "MACD Indicator")

    # TOS
    trades = tos.testPolicy(symbol="JPM", sd=start_date, ed=end_date, sv=100000)

    #synthetic orders
    orders_df = pd.DataFrame(index=trades.index, columns=["Symbol", "Order", "Shares"])
    orders_df["Symbol"] = "JPM"
    orders_df["Order"] = trades.applymap(lambda x: "BUY" if x > 0 else "SELL")
    orders_df["Shares"] = trades.abs()

    #portfolio stats
    portfolio_vals = compute_portvals(orders=orders_df, start_date=start_date, end_date=end_date)
    portfolio_vals = portfolio_vals / portfolio_vals.iloc[0]

    # Benchmark
    benchmark = get_data(["JPM"], pd.date_range(start_date, end_date), colname="Adj Close").drop("SPY", axis=1)
    benchmark["Benchmark"] = benchmark / benchmark.iloc[0]


    plt.plot(benchmark["Benchmark"], label="Benchmark", color="green")
    plt.plot(portfolio_vals, label="TOS Portfolio", color="red")
    plt.legend()
    plt.title("TOS vs Benchmark")
    plt.savefig("TOS_vs_Benchmark.png")
    plt.close()


    daily_returns = portfolio_vals.diff().dropna()
    stats = {
        'Benchmark': {'STD': daily_returns.std(), 'Cumulative Returns': daily_returns.sum(), 'Mean Returns': daily_returns.mean()},
        'TOS Portfolio': {'STD': daily_returns.std(), 'Cumulative Returns': daily_returns.sum(), 'Mean Returns': daily_returns.mean()}
    }
    pd.DataFrame(stats).to_csv("p6_results.txt", sep="\t")
