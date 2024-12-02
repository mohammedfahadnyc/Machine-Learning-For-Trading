import datetime as dt
import numpy as np
import random
import pandas as pd
from StrategyLearner import StrategyLearner  # Ensure StrategyLearner is in your PYTHONPATH
from strategy_evaluation.grade_strategy_learner import compute_portvals
from util import get_data

# Constants
MAX_HOLDINGS = 1000
START_VALUE = 100000

# Define failing test case
test_case = {
    "description": "ML4T-220",
    "insample_args": dict(
        symbol="ML4T-220",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 12, 31),
        sv=START_VALUE,
    ),
    "outsample_args": dict(
        symbol="ML4T-220",
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=START_VALUE,
    ),
    "benchmark": 1.0,
    "impact": 0.0,
    "seed": 1481090000,
}

# Initialize random seed
np.random.seed(test_case["seed"])
random.seed(test_case["seed"])

# Initialize StrategyLearner
learner = StrategyLearner(verbose=True, impact=test_case["impact"])

# Training phase
print("=== Training Phase ===")
learner.add_evidence(**test_case["insample_args"])

# In-sample testing
print("\n=== In-Sample Testing Phase ===")
insample_trades = learner.testPolicy(**test_case["insample_args"])
print(f"In-sample trades:\n{insample_trades}")

# Evaluate in-sample cumulative return
def eval_policy(symbol, trades, startval, sd, ed, market_impact=0.0, commission_cost=0.0):
    orders_df = pd.DataFrame(columns=["Shares", "Order", "Symbol"])
    for row_idx in trades.index:
        nshares = trades.loc[row_idx][0]
        if nshares == 0:
            continue
        order = "sell" if nshares < 0 else "buy"
        new_row = pd.DataFrame(
            [[abs(nshares), order, symbol]],
            columns=["Shares", "Order", "Symbol"],
            index=[row_idx],
        )
        orders_df = orders_df.append(new_row)
    portvals = compute_portvals(
        orders_df, sd, ed, startval, market_impact, commission_cost
    )
    return float(portvals[-1] / portvals[0]) - 1

insample_cr = eval_policy(
    test_case["insample_args"]["symbol"],
    insample_trades,
    test_case["insample_args"]["sv"],
    test_case["insample_args"]["sd"],
    test_case["insample_args"]["ed"],
    market_impact=test_case["impact"],
    commission_cost=0.0,
)
print(f"In-sample cumulative return: {insample_cr}, Benchmark: {test_case['benchmark']}")

# Out-of-sample testing
print("\n=== Out-of-Sample Testing Phase ===")
outsample_trades = learner.testPolicy(**test_case["outsample_args"])
print(f"Out-of-sample trades:\n{outsample_trades}")

# Evaluate out-of-sample cumulative return
outsample_cr = eval_policy(
    test_case["outsample_args"]["symbol"],
    outsample_trades,
    test_case["outsample_args"]["sv"],
    test_case["outsample_args"]["sd"],
    test_case["outsample_args"]["ed"],
    market_impact=test_case["impact"],
    commission_cost=0.0,
)
print(f"Out-of-sample cumulative return: {outsample_cr}, Benchmark: {test_case['benchmark']}")
