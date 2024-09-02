""""""  		  	   		 	   		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
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
  		  	   		 	   		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 	   		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
  		  	   		 	   		  		  		    	 		 		   		 		  
def author():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    return "mfahad7"  # replace tb34 with your Georgia Tech username.
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
def gtid():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    return 903967206  # replace with your GT ID number

def study_group():
    """
    Returns
        A comma separated string of GT_Name of each member of your study group
        # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
    Return type
        str
    """
    return "mfahad7"
  		  	   		 	   		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		 	   		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    result = False  		  	   		 	   		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		 	   		  		  		    	 		 		   		 		  
        result = True  		  	   		 	   		  		  		    	 		 		   		 		  
    return result  		  	   		 	   		  		  		    	 		 		   		 		  

def simulate_episode(win_prob, max_spins=1000, target_winnings=80, bankroll=None):
    """
    Simulate a single episode of the Martingale strategy.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    :param max_spins: The maximum number of spins in an episode, defaults to 1000
    :type max_spins: int, optional
    :param target_winnings: The target winnings to stop the episode, defaults to 80
    :type target_winnings: int, optional
    :param bankroll: The starting bankroll, defaults to None
    :type bankroll: int, optional
    :return: An array representing the winnings over each spin
    :rtype: np.ndarray
    """
    winnings = np.zeros(max_spins + 1)
    current_winnings = 0
    bet = 1

    for i in range(1, max_spins + 1):
        if current_winnings >= target_winnings:
            winnings[i:] = current_winnings
            break

        if bankroll is not None and bet > bankroll + current_winnings:
            bet = bankroll + current_winnings  # Bet the remaining amount if less than the next bet.

        if get_spin_result(win_prob):
            current_winnings += bet
            bet = 1
        else:
            current_winnings -= bet
            bet *= 2

        winnings[i] = current_winnings

        if bankroll is not None and current_winnings <= -bankroll:
            winnings[i:] = -bankroll
            break

    return winnings


def martingale_10_episodes(win_prob):
    """
    Run 10 episodes of the Martingale strategy and plot the results.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    """
    winnings_10 = np.array([simulate_episode(win_prob) for _ in range(10)])

    plt.figure()
    for episode in winnings_10:
        plt.plot(episode)

    plt.title("Martingale Strategy: Winnings over 10 Episodes")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.grid(True)
    plt.savefig('images/martingale_10_episodes.png')
    plt.show()


def martingale_1000_episodes_mean_std(win_prob):
    """
    Run 1000 episodes of the Martingale strategy, calculate the mean and standard deviation of the winnings,
    and plot the results.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    """
    winnings_1000 = np.array([simulate_episode(win_prob) for _ in range(1000)])

    mean_winnings = np.mean(winnings_1000, axis=0)
    std_dev = np.std(winnings_1000, axis=0, ddof=0)

    plt.figure()
    plt.plot(mean_winnings, label='Mean Winnings')
    plt.plot(mean_winnings + std_dev, label='+1 Std Dev', linestyle='--')
    plt.plot(mean_winnings - std_dev, label='-1 Std Dev', linestyle='--')

    plt.title("Martingale Strategy: Mean and Std Dev of Winnings over 1000 Episodes")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.legend()
    plt.grid(True)
    plt.savefig('images/martingale_1000_episodes_mean_std.png')
    plt.show()


def martingale_1000_episodes_median_std(win_prob):
    """
    Run 1000 episodes of the Martingale strategy, calculate the median and standard deviation of the winnings,
    and plot the results.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    """
    winnings_1000 = np.array([simulate_episode(win_prob) for _ in range(1000)])

    median_winnings = np.median(winnings_1000, axis=0)
    std_dev = np.std(winnings_1000, axis=0, ddof=0)

    plt.figure()
    plt.plot(median_winnings, label='Median Winnings')
    plt.plot(median_winnings + std_dev, label='+1 Std Dev', linestyle='--')
    plt.plot(median_winnings - std_dev, label='-1 Std Dev', linestyle='--')

    plt.title("Martingale Strategy: Median and Std Dev of Winnings over 1000 Episodes")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.legend()
    plt.grid(True)
    plt.savefig('images/martingale_1000_episodes_median_std.png')
    plt.show()


def martingale_1000_episodes_bankroll_mean_std(win_prob):
    """
    Run 1000 episodes of the Martingale strategy with a $256 bankroll, calculate the mean and standard deviation
    of the winnings, and plot the results.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    :param bankroll: The starting bankroll, defaults to 256
    :type bankroll: int, optional
    """
    winnings_1000 = np.array([simulate_episode(win_prob, bankroll=256) for _ in range(1000)])

    mean_winnings = np.mean(winnings_1000, axis=0)
    std_dev = np.std(winnings_1000, axis=0, ddof=0)

    plt.figure()
    plt.plot(mean_winnings, label='Mean Winnings')
    plt.plot(mean_winnings + std_dev, label='+1 Std Dev', linestyle='--')
    plt.plot(mean_winnings - std_dev, label='-1 Std Dev', linestyle='--')

    plt.title("Martingale Strategy with $256 Bankroll: Mean and Std Dev of Winnings")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.legend()
    plt.grid(True)
    plt.savefig('images/martingale_1000_episodes_bankroll_mean_std.png')
    plt.show()


def martingale_1000_episodes_bankroll_median_std(win_prob):
    """
    Run 1000 episodes of the Martingale strategy with a $256 bankroll, calculate the median and standard deviation
    of the winnings, and plot the results.

    :param win_prob: The probability of winning a bet
    :type win_prob: float
    :param bankroll: The starting bankroll, defaults to 256
    :type bankroll: int, optional
    """
    winnings_1000 = np.array([simulate_episode(win_prob, bankroll=256) for _ in range(1000)])

    median_winnings = np.median(winnings_1000, axis=0)
    std_dev = np.std(winnings_1000, axis=0, ddof=0)

    plt.figure()
    plt.plot(median_winnings, label='Median Winnings')
    plt.plot(median_winnings + std_dev, label='+1 Std Dev', linestyle='--')
    plt.plot(median_winnings - std_dev, label='-1 Std Dev', linestyle='--')

    plt.title("Martingale Strategy with $256 Bankroll: Median and Std Dev of Winnings")
    plt.xlabel("Spin Number")
    plt.ylabel("Winnings ($)")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.legend()
    plt.grid(True)
    plt.savefig('images/martingale_1000_episodes_bankroll_median_std.png')
    plt.show()

  		  	   		 	   		  		  		    	 		 		   		 		  
def test_code():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once  		  	   		 	   		  		  		    	 		 		   		 		  
    # print(get_spin_result(win_prob))  # test the roulette spin
    # Experiment 1
    martingale_10_episodes(win_prob)  # Figure 1: 10 episodes
    martingale_1000_episodes_mean_std(win_prob)  # Figure 2: 1000 episodes - Mean and Std Dev
    martingale_1000_episodes_median_std(win_prob)  # Figure 3: 1000 episodes - Median and Std Dev

    # Experiment 2
    martingale_1000_episodes_bankroll_mean_std(
        win_prob)  # Figure 4: 1000 episodes with $256 bankroll - Mean and Std Dev
    martingale_1000_episodes_bankroll_median_std(
        win_prob)  # Figure 5: 1000 episodes with $256 bankroll - Median and Std Dev
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	   		  		  		    	 		 		   		 		  
    test_code()  		  	   		 	   		  		  		    	 		 		   		 		  
