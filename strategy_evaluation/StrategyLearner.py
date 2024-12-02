""""""
from qlearning_robot.QLearner import QLearner
import numpy as np
"""  		  	   		 	   		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	   		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	   		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	   		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	   		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   		  		  		    	 		 		   		 		  
or edited.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		 	   		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	   		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 	   		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""  		  	   		 	   		  		  		    	 		 		   		 		  

import datetime as dt
import pandas as pd

import util as ut


class StrategyLearner:
    def __init__(self, verbose=False, impact=0.005, commission=9.95):
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = None

    def add_evidence(self, symbol="IBM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), sv=100000):
        """Train the strategy learner."""
        self.learner = QLearner(num_states=1000, num_actions=3, alpha=0.1, gamma=0.9, rar=0.9, radr=0.99)


        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices = prices_all[symbol]


        indicators = self._calculate_indicators(prices)


        states = self._discretize_states(indicators)

        # Train Q-Learner
        for episode in range(100):
            cash = sv
            holdings = 0
            for i in range(len(prices) - 1):
                state = states.iloc[i]
                action = self.learner.querysetstate(state)
                trade = self._convert_action_to_trade(action, holdings)


                reward = self._calculate_reward(trade, holdings, prices, i)
                holdings += trade
                cash -= trade * prices.iloc[i] + abs(trade) * self.commission + abs(trade) * prices.iloc[i] * self.impact


                new_state = states.iloc[i + 1]
                self.learner.query(new_state, reward)

    def testPolicy(self, symbol="IBM", sd=dt.datetime(2009, 1, 1), ed=dt.datetime(2010, 1, 1), sv=100000):
        """Test the policy learned by StrategyLearner."""
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)
        prices = prices_all[symbol]
        indicators = self._calculate_indicators(prices)
        states = self._discretize_states(indicators)

        trades = pd.DataFrame(index=prices.index, columns=[symbol])
        trades[symbol] = 0

        holdings = 0
        for i in range(len(prices) - 1):
            state = states.iloc[i]
            action = self.learner.querysetstate(state)
            trade = self._convert_action_to_trade(action, holdings)
            trades.iloc[i] = trade
            holdings += trade

        if holdings != 0:
            trades.iloc[-1] = -holdings

        return trades

    def _calculate_indicators(self, prices):
        """Calculate market indicators."""
        sma = prices.rolling(window=20).mean()
        sma_ratio = prices / sma
        rsi = self._calculate_rsi(prices)
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26

        return pd.DataFrame({"SMA": sma_ratio, "RSI": rsi, "MACD": macd}).fillna(0)

    def _calculate_rsi(self, prices):
        """Calculate RSI."""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _discretize_states(self, indicators):
        """Discretize indicators."""
        bins = 10
        sma_bins = pd.qcut(indicators["SMA"], bins, labels=False)
        rsi_bins = pd.qcut(indicators["RSI"], bins, labels=False)
        macd_bins = pd.qcut(indicators["MACD"], bins, labels=False)
        return (sma_bins * 100) + (rsi_bins * 10) + macd_bins

    def _convert_action_to_trade(self, action, holdings):
        """Convert action to trade."""
        max_shares = 1000
        if action == 0:  # Hold
            return 0
        elif action == 1:  # Buy
            return max_shares - holdings
        elif action == 2:  # Sell
            return -holdings
        return 0

    def _calculate_reward(self, trade, holdings, prices, i):
        """Calculate reward."""
        trade_impact = self.impact * abs(trade)
        trade_cost = abs(trade) * prices.iloc[i] + self.commission + trade_impact
        reward = (holdings * (prices.iloc[i + 1] - prices.iloc[i])) - trade_cost
        return reward

    def author(self):
        return "mfahad7"

    def study_group(self):
        return "mfahad7"

def format_trades_for_portvals(trades, symbol):
    """Format trades DataFrame for compute_portvals."""
    trades = trades.copy()
    trades.reset_index(inplace=True)
    trades['Symbol'] = symbol
    trades.rename(columns={symbol: 'Shares'}, inplace=True)  # Rename to 'Shares'
    trades['Order'] = trades['Shares'].apply(lambda x: 'BUY' if x > 0 else ('SELL' if x < 0 else 'HOLD'))
    trades['Shares'] = trades['Shares'].abs()
    return trades

if __name__ == "__main__":
    from marketsim.marketsim import compute_portvals


    strategy_learner = StrategyLearner(verbose=True, impact=0.005, commission=9.95)


    strategy_learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)


    trades = strategy_learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 12, 31),
                                         sv=100000)



    trades = strategy_learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2010, 12, 31),
                                         sv=100000)


    formatted_trades =format_trades_for_portvals(trades, "JPM")


    formatted_trades.set_index('index', inplace=True)
    formatted_trades.index = pd.to_datetime(formatted_trades.index)


    portvals = compute_portvals(formatted_trades, start_val=100000, commission=9.95, impact=0.005)
    portvals = portvals / portvals.iloc[0]


    cr = portvals.iloc[-1] - 1
    daily_returns = portvals.pct_change().dropna()
    adr = daily_returns.mean()
    sddr = daily_returns.std()

    print(f"Cumulative Return: {cr}")
    print(f"Average Daily Return: {adr}")
    print(f"Std of Daily Return: {sddr}")

