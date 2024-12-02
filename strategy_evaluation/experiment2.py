import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
from marketsim.marketsim import compute_portvals
from StrategyLearner import StrategyLearner

def run_strategy(impact, symbol="JPM", sd=dt(2008, 1, 1), ed=dt(2009, 12, 31), sv=100000):
    """
    Runs the Strategy Learner with a given impact value and returns portfolio metrics.

    :param impact: The market impact value to use.
    :param symbol: The stock symbol to trade.
    :param sd: The start date for training.
    :param ed: The end date for testing.
    :param sv: Starting cash value.
    :return: Cumulative return, standard deviation of daily returns, and mean daily return.
    """
    learner = StrategyLearner(verbose=False, impact=impact, commission=9.95)
    learner.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=sv)
    trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)


    trades = trades.reset_index()
    trades['Symbol'] = symbol
    trades.rename(columns={symbol: 'Shares'}, inplace=True)
    trades['Order'] = trades['Shares'].apply(lambda x: 'BUY' if x > 0 else ('SELL' if x < 0 else 'HOLD'))
    trades['Shares'] = trades['Shares'].abs()
    trades.set_index('index', inplace=True)
    trades.index = pd.to_datetime(trades.index)


    portvals = compute_portvals(orders_file=trades, start_val=sv, commission=9.95, impact=impact)
    portvals = portvals / portvals.iloc[0]  # Normalize portfolio values


    cumulative_return = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    daily_returns = portvals.pct_change().dropna()
    std_dev = daily_returns.std()
    mean_daily_return = daily_returns.mean()

    return cumulative_return[0], std_dev[0], mean_daily_return[0]


def experiment2():
    """
    Runs Experiment 2 to evaluate the effect of different impact values on Strategy Learner performance.
    """
    impacts = [0.005, 0.01, 0.02]
    results = []


    for impact in impacts:
        print(f"Running Strategy Learner with impact={impact}...")
        cumulative_return, std_dev, mean_daily_return = run_strategy(impact)
        results.append((impact, cumulative_return, std_dev, mean_daily_return))


    results_df = pd.DataFrame(results, columns=["Impact", "Cumulative Return", "Std Dev of Daily Returns", "Mean Daily Return"])
    print("\nResults:")
    print(results_df)


    plt.figure(figsize=(10, 6))
    plt.plot(results_df["Impact"], results_df["Cumulative Return"], marker='o', label="Cumulative Return")
    plt.plot(results_df["Impact"], results_df["Std Dev of Daily Returns"], marker='o', label="Std Dev of Daily Returns")
    plt.plot(results_df["Impact"], results_df["Mean Daily Return"], marker='o', label="Mean Daily Return")
    plt.xlabel("Impact")
    plt.ylabel("Metrics")
    plt.title("Effect of Impact on Strategy Learner Performance")
    plt.legend()
    plt.grid()
    plt.savefig("images/experiment2_impact_vs_performance.png")
    plt.show()

    print("Experiment 2 completed. Results saved to 'images/experiment2_impact_vs_performance.png'.")


if __name__ == "__main__":
    experiment2()
