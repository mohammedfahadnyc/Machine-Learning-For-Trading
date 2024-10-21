import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from util import get_data
from indicators import golden_cross, calculate_ema, rsi, mfi, macd
import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals


def author():
    return "mfahad7"  # replace with your Georgia Tech username


def plot_ind(df, plot_title):
    """
    General function to plot a Series or DataFrame.
    """
    fig = plt.figure()

    # Check if the input is a DataFrame or a Series
    if isinstance(df, pd.DataFrame):
        plt.plot(df)
        plt.legend(df.columns)  # Use column names for DataFrame
    else:
        plt.plot(df)
        plt.legend([df.name if df.name else 'Indicator'])  # Use a generic label if it's a Series

    plt.xlabel("Date")
    plt.ylabel("Price, Index Value ")
    plt.title(plot_title)
    fig.autofmt_xdate()
    plt.savefig(plot_title + ".png")
    plt.close()


def split_plot_ind(df, plot_title):
    """
    Function to plot JPM price along with the indicator values in two subplots.
    Handles both DataFrames and Series.
    """
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False)

    # Ensure we are working with a DataFrame
    if isinstance(df, pd.Series):
        df = df.to_frame(name="Indicator")

    plt.title("JPM Stock Price (Above) vs " + plot_title + " (Below)")

    # Subplot 1: JPM Stock Price
    axes[0].plot(adj_close.index, adj_close, label="JPM Stock Price")
    axes[0].legend(loc="upper left")

    # Subplot 2: Indicator
    axes[1].plot(df.index, df.iloc[:, 0], label=plot_title)
    axes[1].legend(loc="upper left")
    axes[1].set_ylabel("Index Value, Price")

    plt.xlabel("Date")
    fig.autofmt_xdate()
    plt.savefig(plot_title + ".png")
    plt.close()


if __name__ == "__main__":
    # Step 1: Setup date range and symbol
    sd = dt.date(2008, 1, 1)
    ed = dt.date(2009, 12, 31)
    symbols = ["JPM"]  # List of symbols (in this case, just JPM)

    # Step 2: Fetch price data (including High, Low, Volume, Adj Close)
    high = get_data(symbols, pd.date_range(sd, ed), addSPY=True, colname="High").drop(columns=["SPY"])
    low = get_data(symbols, pd.date_range(sd, ed), addSPY=True, colname="Low").drop(columns=["SPY"])
    volume = get_data(symbols, pd.date_range(sd, ed), addSPY=True, colname="Volume").drop(columns=["SPY"])
    adj_close = get_data(symbols, pd.date_range(sd, ed), addSPY=True, colname="Adj Close").drop(columns=["SPY"])

    # Ensure "adj_close" is a Series, not DataFrame, for JPM
    adj_close = adj_close["JPM"]  # Extract just the "JPM" column to ensure it's properly indexed

    # Step 3: Indicators
    gdc = golden_cross(adj_close)
    plot_ind(gdc, "Golden Cross")

    ema = calculate_ema(adj_close, 50)
    plot_ind(ema, "Exponential Moving Average")

    rsi_values = rsi(adj_close)
    split_plot_ind(rsi_values, "RSI")

    mfi_values = mfi(adj_close, low, high, volume)
    split_plot_ind(mfi_values, "Money Flow")

    macd_values = macd(adj_close)
    split_plot_ind(macd_values, "MACD")

    # Step 4: Theoretically Optimal Strategy (TOS)
    df_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    # Step 5: Create orders file format from TOS output
    orders = pd.DataFrame(index=df_trades.index, columns=["Symbol", "Order", "Shares"])
    orders["Symbol"] = "JPM"
    orders["Order"] = df_trades.applymap(lambda x: "BUY" if x > 0 else "SELL" if x < 0 else "HOLD")
    orders["Shares"] = df_trades.abs()

    # Step 6: Compute Portfolio Values based on trades from TOS
    port_value = compute_portvals(df_trades, start_val=100000)

    # Step 7: Benchmark Portfolio
    benchmark = get_data(["JPM"], pd.date_range(sd, ed), addSPY=True, colname="Adj Close").drop(columns="SPY")
    benchmark = 1000 * benchmark / benchmark.iloc[0]  # Normalize benchmark to 1000 shares

    # Step 8: Compare TOS vs. Benchmark
    port_value = port_value / port_value.iloc[0]  # Normalize TOS portfolio to match benchmark
    data = pd.concat([benchmark, port_value], axis=1)
    data.columns = ["Benchmark", "TOS Portfolio"]

    # Plot TOS Portfolio vs Benchmark
    fig = plt.figure()
    plt.plot(data["Benchmark"], label="Benchmark", color="green")
    plt.plot(data["TOS Portfolio"], label="TOS Portfolio", color="red")
    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.title("TOS Portfolio vs Benchmark")
    fig.autofmt_xdate()
    plt.savefig("TOS_Portfolio_vs_Benchmark.png")
    plt.close()

    # Step 9: Calculate and print performance stats
    daily_rets = data.pct_change().dropna()

    # Benchmark performance
    bench_std = daily_rets["Benchmark"].std()
    bench_cum_ret = (data["Benchmark"][-1] / data["Benchmark"][0]) - 1
    bench_mean_ret = daily_rets["Benchmark"].mean()

    # TOS Portfolio performance
    port_std = daily_rets["TOS Portfolio"].std()
    port_cum_ret = (data["TOS Portfolio"][-1] / data["TOS Portfolio"][0]) - 1
    port_mean_ret = daily_rets["TOS Portfolio"].mean()

    # Output performance stats to a file
    with open("p6_results.txt", "w") as f:
        f.write("Performance Metrics\n")
        f.write(
            f"Benchmark: Std: {bench_std:.6f}, Cumulative Return: {bench_cum_ret:.6f}, Mean Return: {bench_mean_ret:.6f}\n")
        f.write(
            f"TOS Portfolio: Std: {port_std:.6f}, Cumulative Return: {port_cum_ret:.6f}, Mean Return: {port_mean_ret:.6f}\n")
