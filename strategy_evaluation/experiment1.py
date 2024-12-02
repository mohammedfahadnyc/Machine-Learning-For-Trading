import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner, format_trades_for_portvals
from marketsim.marketsim import compute_portvals

def run_strategy(strategy, sd, ed, start_cash=100000, commission=9.95, impact=0.005,format_for_portvals=False):
    """Runs a given strategy and returns portfolio values."""
    trades = strategy.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=start_cash)
    print("Trades DataFrame:")
    print(trades.head())
    print("Trades Columns:", trades.columns)
    if format_for_portvals:
        formatted_trades = format_trades_for_portvals(trades, "JPM")
        formatted_trades.set_index('index', inplace=True)
        formatted_trades.index = pd.to_datetime(formatted_trades.index)
        trades = formatted_trades
    portvals = compute_portvals(orders_file=trades, start_val=start_cash, commission=commission, impact=impact)
    return portvals


def print_metrics(portvals, label):
    """Prints the performance metrics for a given portfolio."""
    portvals = portvals.squeeze()  # Ensure portvals is a Series
    cum_return = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    daily_returns = portvals.pct_change().dropna()
    std_dev = daily_returns.std()
    mean_daily_return = daily_returns.mean()
    print(f"\n{label}:")
    print(f"Cumulative Return: {cum_return:.4f}")
    print(f"Standard Deviation of Daily Returns: {std_dev:.4f}")
    print(f"Mean Daily Return: {mean_daily_return:.4f}")

def plot_portfolio(portvals_manual, portvals_learner, label, filename):
    """Plots portfolio values for manual and strategy learners."""
    plt.figure(figsize=(10, 6))
    plt.plot(portvals_manual.index, portvals_manual / portvals_manual.iloc[0], label="Manual Strategy")
    plt.plot(portvals_learner.index, portvals_learner / portvals_learner.iloc[0], label="Strategy Learner")
    plt.title(f"Portfolio Performance ({label})")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.grid()
    plt.savefig(f"images/{filename}")
    plt.close()

def experiment1():
    in_sample_start = dt.datetime(2008, 1, 1)
    in_sample_end = dt.datetime(2009, 12, 31)
    out_sample_start = dt.datetime(2010, 1, 1)
    out_sample_end = dt.datetime(2011, 12, 31)
    start_cash = 100000
    commission = 9.95
    impact = 0.005


    manual_strategy = ManualStrategy(verbose=False, impact=impact, commission=commission)
    print("\nRunning Manual Strategy (In-Sample)...")
    manual_portvals_in = run_strategy(manual_strategy, in_sample_start, in_sample_end)
    print_metrics(manual_portvals_in, "Manual Strategy (In-Sample)")

    print("\nRunning Manual Strategy (Out-of-Sample)...")
    manual_portvals_out = run_strategy(manual_strategy, out_sample_start, out_sample_end)
    print_metrics(manual_portvals_out, "Manual Strategy (Out-of-Sample)")


    strategy_learner = StrategyLearner(verbose=False, impact=impact, commission=commission)
    print("\nTraining Strategy Learner...")
    strategy_learner.add_evidence(symbol="JPM", sd=in_sample_start, ed=in_sample_end, sv=start_cash)

    print("\nRunning Strategy Learner (In-Sample)...")
    learner_portvals_in = run_strategy(strategy_learner, in_sample_start, in_sample_end,format_for_portvals=True)
    print_metrics(learner_portvals_in, "Strategy Learner (In-Sample)")

    print("\nRunning Strategy Learner (Out-of-Sample)...")
    learner_portvals_out = run_strategy(strategy_learner, out_sample_start, out_sample_end,format_for_portvals=True)
    print_metrics(learner_portvals_out, "Strategy Learner (Out-of-Sample)")


    print("\nGenerating and saving plots...")
    plot_portfolio(manual_portvals_in, learner_portvals_in, "In-Sample", "in_sample_performance.png")
    plot_portfolio(manual_portvals_out, learner_portvals_out, "Out-of-Sample", "out_of_sample_performance.png")
    print("Plots saved in the 'images' folder.")

if __name__ == "__main__":
    experiment1()

