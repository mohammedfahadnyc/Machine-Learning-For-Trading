""""""
import random

"""  		  	   		 	   		  		  		    	 		 		   		 		  
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
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
  		  	   		 	   		  		  		    	 		 		   		 		  
Student Name: Mohammed Fahad (replace with your name)  		  	   		 	   		  		  		    	 		 		   		 		  
GT User ID: mfahad7 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 903967206 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""



import numpy as np


class QLearner(object):
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		 	   		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		 	   		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		 	   		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		 	   		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		 	   		  		  		    	 		 		   		 		  
    """
    def __init__(self, num_states=100, num_actions=4, alpha=0.2, gamma=0.9,
                 rar=0.5, radr=0.99, dyna=0, verbose=False):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.rar = rar          # Random action rate
        self.radr = radr        # Random action decay rate
        self.dyna = dyna        # Number of Dyna iterations
        self.verbose = verbose

        # Q-table
        self.q_table = np.zeros((num_states, num_actions))

        #replay buffer Dyna-Q
        self.experience = [] if dyna > 0 else None


        self.s = 0
        self.a = 0

    def querysetstate(self, s):
        """ Update the state without updating the Q-table """


        self.s = s

        # Decide if random action
        if random.uniform(0, 1) < self.rar:
            action = random.randint(0, self.num_actions - 1)  # Random action
        else:
            action = np.argmax(self.q_table[s])  # based on Q-table

        self.a = action

        if self.verbose:
            print(f"querysetstate - State: {s}, Action: {action}")

        return action

    def query(self, s_prime, r):
        """ Update the Q table and return an action """

        s = self.s
        a = self.a
        alpha = self.alpha
        gamma = self.gamma

        # Update Q-tabl
        self.q_table[s, a] = (1 - alpha) * self.q_table[s, a] + alpha * (r + gamma * np.max(self.q_table[s_prime]))

        if self.dyna > 0:
            self.experience.append((s, a, s_prime, r))

        # Decide if random action
        if random.uniform(0, 1) < self.rar:
            action = random.randint(0, self.num_actions - 1)
        else:
            action = np.argmax(self.q_table[s_prime])

        # Decay action rate
        self.rar *= self.radr

        # Perform Dyna-Q updates
        if self.dyna > 0:
            for _ in range(self.dyna):
                # random experience from  buffer
                s_dyna, a_dyna, s_prime_dyna, r_dyna = random.choice(self.experience)
                # Update Q-table
                self.q_table[s_dyna, a_dyna] = (1 - alpha) * self.q_table[s_dyna, a_dyna] + \
                                                alpha * (r_dyna + gamma * np.max(self.q_table[s_prime_dyna]))


        self.s = s_prime
        self.a = action

        if self.verbose:
            print(f"query - s: {s}, a: {a}, r: {r}, s': {s_prime}, next a: {action}, rar: {self.rar}")

        return action

    def author(self):
        return 'mfahad7'  # GT username

    def study_group(self):
        """
        Returns
            A comma separated string of GT_Name of each member of your study group
            # Example: "gburdell3, jdoe77, tbalch7" or "gburdell3" if a single individual working alone
        Return type
            str
        """
        return "mfahad7"


if __name__ == "__main__":
    print("Remember Q from Star Trek? Well, this isn't him")
