import pandas as pd
import numpy as np

def author():
    return 'mfahad7'  # Your Georgia Tech username

def calculate_sma(df, window):
    """
    Calculate Simple Moving Average (SMA)
    """
    return df.rolling(window=window).mean()

def golden_cross(df, short_window=50, long_window=200):
    """
    Golden/Death Cross Indicator: Short-term SMA crossing long-term SMA.
    Buy signal: Short-term SMA crosses above long-term SMA.
    Sell signal: Short-term SMA crosses below long-term SMA.
    """
    short_sma = calculate_sma(df, short_window)
    long_sma = calculate_sma(df, long_window)

    # Drop any NaN values from the SMA calculations
    short_sma = short_sma.dropna()
    long_sma = long_sma.dropna()

    # Align the indices of short_sma and long_sma
    common_index = short_sma.index.intersection(long_sma.index)
    short_sma = short_sma.reindex(common_index)
    long_sma = long_sma.reindex(common_index)

    # Create a signal Series with the same index
    signal = pd.Series(0.0, index=common_index)

    # Buy signal when short-term SMA is greater than long-term SMA
    signal[short_sma > long_sma] = 1

    # Sell signal when short-term SMA is less than long-term SMA
    signal[short_sma < long_sma] = -1

    return signal


def calculate_ema(df, window):
    """
    Calculate Exponential Moving Average (EMA)
    """
    return df.ewm(span=window, adjust=False).mean()

def rsi(df, window=14):
    """
    Calculate Relative Strength Index (RSI)
    """
    delta = df.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=df.index)

def mfi(df, high, low, volume, window=14):
    """
    Money Flow Index (MFI)
    """
    typical_price = (df + high + low) / 3
    money_flow = typical_price * volume
    positive_flow = money_flow[typical_price.diff() > 0].fillna(0)
    negative_flow = money_flow[typical_price.diff() < 0].fillna(0)
    money_flow_ratio = positive_flow.rolling(window=window).sum() / negative_flow.rolling(window=window).sum()
    mfi = 100 - (100 / (1 + money_flow_ratio))
    return mfi

def macd(df, short_window=12, long_window=26, signal_window=9):
    """
    Moving Average Convergence Divergence (MACD)
    """
    short_ema = calculate_ema(df, short_window)
    long_ema = calculate_ema(df, long_window)
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    return pd.Series(macd_histogram, index=df.index)

# You can add more indicators here if needed or modify the parameters of the ones above.

# if __name__ == "__main__":
#     # Example to run and test the indicators
#     data = pd.read_csv("data/JPM.csv", index_col="Date", parse_dates=True)
#     close_prices = data['Adj Close']
#
#     # Example usage of indicators
#     golden_cross_signal = golden_cross(close_prices)
#     ema = calculate_ema(close_prices, 50)
#     rsi_values = rsi(close_prices)
#     mfi_values = mfi(close_prices, data['High'], data['Low'], data['Volume'])
#     macd_histogram = macd(close_prices)
#
#     # Here you can generate plots and save them, e.g., using matplotlib
