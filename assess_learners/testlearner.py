""""""  		  	   		 	   		  		  		    	 		 		   		 		  
"""  		  	   		 	   		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
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
"""
import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl

def run_experiment_dt_learner(train_x, train_y, test_x, test_y):
    rmse_in_sample = []
    rmse_out_sample = []
    for i in range(1, 21):
        learner = dt.DTLearner(leaf_size=i, verbose=False)
        learner.add_evidence(train_x, train_y)
        pred_y_in = learner.query(train_x)
        rmse_in = math.sqrt(((train_y - pred_y_in) ** 2).sum() / train_y.shape[0])
        rmse_in_sample.append(rmse_in)

        pred_y_out = learner.query(test_x)
        rmse_out = math.sqrt(((test_y - pred_y_out) ** 2).sum() / test_y.shape[0])
        rmse_out_sample.append(rmse_out)

    plt.plot(rmse_in_sample)
    plt.plot(rmse_out_sample)
    plt.title("DTLearner: RMSE vs Leaf Size")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend(["In-Sample RMSE", "Out-of-Sample RMSE"])
    plt.savefig("dt_learner_rmse_vs_leaf_size.png")
    plt.close()

def run_experiment_bag_learner(train_x, train_y, test_x, test_y):
    rmse_in_sample = []
    rmse_out_sample = []
    for i in range(1, 21):
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size": i}, bags=10, boost=False, verbose=False)
        learner.add_evidence(train_x, train_y)
        pred_y_in = learner.query(train_x)
        rmse_in = math.sqrt(((train_y - pred_y_in) ** 2).sum() / train_y.shape[0])
        rmse_in_sample.append(rmse_in)

        pred_y_out = learner.query(test_x)
        rmse_out = math.sqrt(((test_y - pred_y_out) ** 2).sum() / test_y.shape[0])
        rmse_out_sample.append(rmse_out)

    plt.plot(rmse_in_sample)
    plt.plot(rmse_out_sample)
    plt.title("BagLearner: RMSE vs Leaf Size with 10 Bags")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.legend(["In-Sample RMSE", "Out-of-Sample RMSE"])
    plt.savefig("bag_learner_rmse_vs_leaf_size.png")
    plt.close()

def run_experiment_dt_vs_rt(train_x, train_y):
    time_dt = []
    time_rt = []
    mae_dt = []
    mae_rt = []

    for i in range(1, 21):
        start_dt = time.time()
        learner_dt = dt.DTLearner(leaf_size=i, verbose=False)
        learner_dt.add_evidence(train_x, train_y)
        end_dt = time.time()
        time_dt.append(end_dt - start_dt)

        start_rt = time.time()
        learner_rt = rt.RTLearner(leaf_size=i, verbose=False)
        learner_rt.add_evidence(train_x, train_y)
        end_rt = time.time()
        time_rt.append(end_rt - start_rt)

        pred_y_dt = learner_dt.query(train_x)
        mae_dt.append(np.mean(np.abs(train_y - pred_y_dt)) * 100)

        pred_y_rt = learner_rt.query(train_x)
        mae_rt.append(np.mean(np.abs(train_y - pred_y_rt)) * 100)

    plt.plot(time_dt)
    plt.plot(time_rt)
    plt.title("Training Time Comparison: DTLearner vs RTLearner")
    plt.xlabel("Leaf Size")
    plt.ylabel("Training Time (seconds)")
    plt.legend(["DTLearner Training Time", "RTLearner Training Time"])
    plt.savefig("dt_vs_rt_training_time.png")
    plt.close()

    plt.plot(mae_dt)
    plt.plot(mae_rt)
    plt.title("Mean Absolute Error Comparison: DTLearner vs RTLearner")
    plt.xlabel("Leaf Size")
    plt.ylabel("Mean Absolute Error (MAE)")
    plt.legend(["DTLearner MAE", "RTLearner MAE"])
    plt.savefig("dt_vs_rt_mae.png")
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)

    data = np.genfromtxt(sys.argv[1], delimiter=',')
    data = data[1:, 1:]  # remove date and header

    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    train_x = data[:train_rows, 0:-1]
    train_y = data[:train_rows, -1]
    test_x = data[train_rows:, 0:-1]
    test_y = data[train_rows:, -1]

    run_experiment_dt_learner(train_x, train_y, test_x, test_y)
    run_experiment_bag_learner(train_x, train_y, test_x, test_y)
    run_experiment_dt_vs_rt(train_x, train_y)
