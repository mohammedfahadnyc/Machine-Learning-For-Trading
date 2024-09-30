""""""  		  	   		 	   		  		  		    	 		 		   		 		  
"""  		  	   		 	   		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		 	   		  		  		    	 		 		   		 		  
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
  		  	   		 	   		  		  		    	 		 		   		 		  
import numpy as np
import numpy.ma as ma

class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def add_evidence(self, data_x, data_y):
        data = np.hstack((data_x, data_y.reshape(-1, 1)))
        self.tree = self.build_tree(data)

    def build_tree(self, data):
        data_y = data[:, -1]
        if data.shape[0] <= self.leaf_size or len(data.shape) == 1:
            return np.array([['leaf', np.mean(data_y), -1, -1]])
        elif np.all(data_y == data[0, -1]):
            return np.array([['leaf', data[0, -1], -1, -1]])
        else:
            best_i = 0
            highest_corr = -1
            for i in range(data.shape[1] - 1):
                corr = ma.corrcoef(ma.masked_invalid(data[:, i]), ma.masked_invalid(data_y))[0, 1]
                corr = abs(corr)
                if corr > highest_corr:
                    highest_corr = corr
                    best_i = i
            split_val = np.median(data[:, best_i], axis=0)
            if split_val == max(data[:, best_i]):
                return np.array([['leaf', np.mean(data_y), -1, -1]])
            left_tree = self.build_tree(data[data[:, best_i] <= split_val])
            right_tree = self.build_tree(data[data[:, best_i] > split_val])
            root = np.array([[best_i, split_val, 1, left_tree.shape[0] + 1]])
            decision_tree = np.vstack((np.vstack((root, left_tree)), right_tree))
            return decision_tree

    def query(self, points):
        results = []
        for i in range(points.shape[0]):
            node = 0
            while self.tree[node, 0] != 'leaf':
                index = self.tree[node, 0]
                split_val = self.tree[node, 1]
                if points[i, int(float(index))] <= float(split_val):
                    left = int(float(self.tree[node, 2]))
                    node += left
                else:
                    right = int(float(self.tree[node, 3]))
                    node += right
            results.append(float(self.tree[node, 1]))
        return np.array(results)

    def author(self):
        return "mfahad7"

    def study_group(self):
        return "mfahad7"

  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	   		  		  		    	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  		  	   		 	   		  		  		    	 		 		   		 		  
