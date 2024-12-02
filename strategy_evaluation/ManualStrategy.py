import pandas as pd
import numpy as np
import datetime as dt


class ManualStrategy:
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission

    def add_evidence(self, symbol="IBM", sd=None, ed=None, sv=100000):
        """No training is needed for manual strategies."""
        pass

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):

        dates = pd.date_range(sd, ed)
        prices_all = self._get_data([symbol], dates)
        prices = prices_all[symbol]


        indicators = self._calculate_indicators(prices)


        trades = pd.DataFrame(index=prices.index, columns=["Shares", "Symbol", "Order"])
        trades["Shares"] = 0
        trades["Symbol"] = symbol


        for i in range(1, len(prices)):
            if indicators["RSI"].iloc[i] < 30 and trades["Shares"].iloc[i - 1] == 0:
                trades.loc[prices.index[i], "Shares"] = 1000
            elif indicators["RSI"].iloc[i] > 70 and trades["Shares"].iloc[i - 1] > 0:
                trades.loc[prices.index[i], "Shares"] = -1000

            if indicators["MACD"].iloc[i] > indicators["Signal"].iloc[i] and trades["Shares"].iloc[i - 1] <= 0:
                trades.loc[prices.index[i], "Shares"] = 1000
            elif indicators["MACD"].iloc[i] < indicators["Signal"].iloc[i] and trades["Shares"].iloc[i - 1] > 0:
                trades.loc[prices.index[i], "Shares"] = -1000

            if indicators["GoldenCross"].iloc[i] and trades["Shares"].iloc[i - 1] <= 0:
                trades.loc[prices.index[i], "Shares"] = 1000
            elif not indicators["GoldenCross"].iloc[i] and trades["Shares"].iloc[i - 1] > 0:
                trades.loc[prices.index[i], "Shares"] = -1000

        #  'Order' column
        trades["Order"] = trades["Shares"].apply(lambda x: "BUY" if x > 0 else ("SELL" if x < 0 else "HOLD"))


        return trades

    def _calculate_indicators(self, prices):
        """Helper method to calculate RSI, MACD, and Golden Cross."""
        # RSI
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # MACD
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        # Golden Cross
        sma20 = prices.rolling(window=20).mean()
        sma50 = prices.rolling(window=50).mean()
        golden_cross = sma20 > sma50

        return pd.DataFrame({
            "RSI": rsi,
            "MACD": macd,
            "Signal": signal,
            "GoldenCross": golden_cross
        })

    def _get_data(self, symbols, dates):
        """Simulates data fetching; replace with actual implementation."""
        np.random.seed(42)
        data = pd.DataFrame(
            data=np.random.uniform(low=50, high=150, size=(len(dates), len(symbols))),
            index=dates, columns=symbols
        )
        return data

    def author(self):
        return "mfahad7"

    def study_group(self):
        return "mfahad7"


if __name__ == "__main__":
    manual_strategy = ManualStrategy(verbose=True)
    trades = manual_strategy.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2008, 12, 31))
    print(trades.head())
