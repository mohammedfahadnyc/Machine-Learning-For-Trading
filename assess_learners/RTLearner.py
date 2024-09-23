import numpy as np
import random

class RTLearner(object):
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
            best_i = random.randint(0, data.shape[1] - 2)
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
