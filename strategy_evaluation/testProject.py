from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner
from experiment1 import experiment1
from experiment2 import experiment2
import datetime as dt

def testproject():
    # Define the parameters
    symbol = "JPM"
    in_sample_start = dt.datetime(2008, 1, 1)
    in_sample_end = dt.datetime(2009, 12, 31)
    out_sample_start = dt.datetime(2010, 1, 1)
    out_sample_end = dt.datetime(2011, 12, 31)
    start_cash = 100000
    commission = 9.95
    impact = 0.005

    print("Running Manual Strategy...")
    manual_strategy = ManualStrategy(verbose=False, impact=impact, commission=commission)
    manual_in_trades = manual_strategy.testPolicy(symbol, in_sample_start, in_sample_end, start_cash)
    manual_out_trades = manual_strategy.testPolicy(symbol, out_sample_start, out_sample_end, start_cash)

    print("Running Strategy Learner...")
    strategy_learner = StrategyLearner(verbose=False, impact=impact, commission=commission)
    strategy_learner.add_evidence(symbol, in_sample_start, in_sample_end, start_cash)
    learner_in_trades = strategy_learner.testPolicy(symbol, in_sample_start, in_sample_end, start_cash)
    learner_out_trades = strategy_learner.testPolicy(symbol, out_sample_start, out_sample_end, start_cash)

    print("Running Experiment 1...")
    experiment1()

    print("Running Experiment 2...")
    experiment2()

if __name__ == "__main__":
    testproject()
