import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from util import get_data


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "mfahad7"


def generate_plot(data, title):
    # Create plot figure
    plt.figure()
    plt.plot(data)
    plt.legend(data.columns)
    plt.xlabel("Date")
    plt.ylabel("Price / Indicator Value")
    plt.title(title)
    plt.gcf().autofmt_xdate()
    plt.savefig(f"{title}.png")
    plt.close()


def generate_split_plot(data, title):
    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.suptitle(f"Stock Price vs {title}")

    # Plot 1: Stock Price
    axes[0].plot(data["JPM"])
    axes[0].set_ylabel("Stock Price")

    # Plot 2: Indicator Values
    axes[1].plot(data.iloc[:, 1:])
    axes[1].set_ylabel("Indicator Value")
    axes[1].set_xlabel("Date")

    plt.gcf().autofmt_xdate()
    plt.savefig(f"{title}.png")
    plt.close()


def calculate_golden_cross(data):
    result_df = data.copy()
    result_df["SMA_20"] = data.rolling(window=20).mean()
    result_df["SMA_50"] = data.rolling(window=50).mean()
    return result_df.dropna()


def calculate_ema(data, window=30):
    ema_df = data.copy()
    ema_df["EMA"] = data.ewm(span=window).mean()
    return ema_df.dropna()


def compute_rsi(data, window=14):
    rsi_df = data.copy()
    delta = rsi_df.pct_change()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi_df["RSI"] = 100 - (100 / (1 + rs))

    rsi_df["Upper_Bound"] = 70
    rsi_df["Lower_Bound"] = 30
    return rsi_df.dropna()


def calculate_money_flow(adj_close, low, high, volume):
    mf_df = adj_close.copy()
    typical_price = (low + high + adj_close) / 3

    delta = typical_price.diff()
    sign = delta.apply(np.sign)

    raw_money_flow = sign * volume * typical_price
    pos_flow = raw_money_flow.clip(lower=0)
    neg_flow = -raw_money_flow.clip(upper=0)

    pos_flow_sum = pos_flow.rolling(window=14).sum()
    neg_flow_sum = neg_flow.rolling(window=14).sum()

    money_flow_ratio = pos_flow_sum / neg_flow_sum
    mf_df["Money_Flow"] = 100 - (100 / (1 + money_flow_ratio))
    mf_df["Upper_Bound"] = 80
    mf_df["Lower_Bound"] = 20

    return mf_df.dropna()


def compute_macd(data, short_window=12, long_window=26):
    macd_df = data.copy()

    short_ema = data.ewm(span=short_window).mean()
    long_ema = data.ewm(span=long_window).mean()

    macd_df["MACD"] = short_ema - long_ema
    macd_df["Signal"] = macd_df["MACD"].ewm(span=9).mean()
    return macd_df.dropna()
