""""""  		  	   		 	   		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
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
GT User ID: mfahad7 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 903967206 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		 	   		  		  		    	 		 		   		 		  
import os  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 	   		  		  		    	 		 		   		 		  
from util import get_data, plot_data

""""""
"""MC2-P1: Market simulator.  		  	   		 	   		  		  		    	 		 		   		 		  

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
import os

import numpy as np

import pandas as pd
from util import get_data, plot_data

import datetime as dt
import pandas as pd
from util import get_data


def author():
    return 'mfahad7'  # Replace with your GT username


def study_group():
    """
    Returns
        A comma separated string of GT_Name of each member of your study group
        # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
    Return type
        str
    """
    return "mfahad7"


def compute_portvals(
        orders_file="./orders/orders.csv",
        start_val=1000000,
        commission=9.95,
        impact=0.005,
):
    """
    Simulates the portfolio values over time, given a set of trade orders.

    :param orders_file: Path to the CSV file containing trade orders.
    :type orders_file: str or file object
    :param start_val: Initial cash value in the portfolio.
    :type start_val: int
    :param commission: The fixed commission cost per trade.
    :type commission: float
    :param impact: The market impact factor affecting prices when trading.
    :type impact: float
    :return: DataFrame with the portfolio values indexed by date.
    :rtype: pandas.DataFrame
    """

    # Reading orders file
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True)

    # simulation start and end  based on the orders file
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()

    # list of symbols to trade
    symbols = orders_df['Symbol'].unique()

    # price for all symbols
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices['Cash'] = 1.0  # column for transaction tracking

    # trades and holdings df
    trades = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    holdings = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    holdings['Cash'].iloc[0] = start_val  # initial cash position

    for date, order in orders_df.iterrows():
        symbol = order['Symbol']
        shares = order['Shares']
        if order['Order'] == 'BUY':
            trade_impact = 1
        else:
            trade_impact = -1

        # adjusted close price for the stock
        price = prices.at[date, symbol]

        adjusted_price = price * (1 + impact * trade_impact)

        # update trades
        trade_cost = trade_impact * shares * adjusted_price
        trades.at[date, symbol] += trade_impact * shares
        trades.at[date, 'Cash'] -= (trade_cost + commission)

    # Update holdings
    holdings.iloc[0] = holdings.iloc[0] + trades.iloc[0]
    for i in range(1, len(holdings)):
        holdings.iloc[i] = holdings.iloc[i - 1] + trades.iloc[i]

    # portfolio values
    portfolio_values = (holdings * prices).sum(axis=1)

    return pd.DataFrame(portfolio_values, columns=['Portfolio Value'])


def test_code():
    """
    Helper function to test the compute_portvals function.
    """
    # Example orders file and starting value
    orders_file = "./orders/orders-01.csv"
    starting_value = 1000000

    portvals = compute_portvals(orders_file=orders_file, start_val=starting_value)

    if isinstance(portvals, pd.DataFrame):
        print(portvals.head())
    else:
        print("Error: compute_portvals should return a DataFrame")


if __name__ == "__main__":
    test_code()
