import numpy as np
from scipy.stats import gaussian_kde

from distribution import Distribution

class NPDistribution(Distribution):
    def __init__(self):
        self.definite_points = []
        self.possible_points = []
        self.distribution = None

    '''
    Returns the probability mass between values a and b, a < b
    '''
    def cdf(self, a, b):
        assert a <= b

        # get rid of this
        return 0.5

    '''
    Include a Gaussian distribution centered at mu. 'weight' is in between
    0 and 1 and represents the confidence that this point belongs in this
    distribution.
    '''
    def update(self, mu, weight):
        assert 0 <= weight <= 1

        if weight == 1:
            self.definite_points.append(mu)
        else:
            self.possible_points.append((mu, weight))

        # turn into an array for numpy's purposes
        a = np.array(self.possible_points)

        # want to keep if weight is greater than random number
        mask = a[:, 1] > np.random.rand(len(possible_points))
        sampled = a[:, 0][mask]

        concatenated = np.concatenate(np.array(self.definite_points), sampled)

        self.distribution = gaussian_kde(concatenated)

    '''
    Samples a point from this distribution between values a and b.
    '''
    def sample(self, a, b):
        assert a <= b

        # get rid of this
        return (a + b) / 2.0
