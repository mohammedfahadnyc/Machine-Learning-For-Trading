import numpy as np

class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = [learner(**kwargs) for _ in range(bags)]

    def add_evidence(self, data_x, data_y):
        rows = data_x.shape[0]
        for learner in self.learners:
            i = np.random.choice(rows, size=rows)
            learner.add_evidence(data_x[i], data_y[i])

    def query(self, points):
        results = np.mean([learner.query(points) for learner in self.learners], axis=0)
        return results

    def author(self):
        return "mfahad7"

    def study_group(self):
        return "mfahad7"
