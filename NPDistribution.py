import random

import numpy as np
from scipy.integrate import cumtrapz
from scipy.stats import gaussian_kde

from distribution import Distribution

class NPDistribution(Distribution):
    def __init__(self):
        self.definite_points = []
        self.possible_points = []
        self.distribution = None

    def __len__(self):
        return len(self.definite_points)

    '''
    Returns the probability mass between values a and b, a < b
    '''
    def cdf(self, a, b):
        return self.distribution.integrate_box_1d(a, b)


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

        if self.possible_points != []:
            # turn into an array for numpy's purposes
            a = np.array(self.possible_points)

            # want to keep if weight is greater than random number
            mask = a[:, 1] > np.random.rand(len(possible_points))
            sampled = a[:, 0][mask]

            cat = np.concatenate(np.array(self.definite_points), sampled)
        else:
            cat = np.array(self.definite_points)

        # THIS IS AN UGLY HACK
        if cat.size == 1:
            cat = np.array([cat[0], cat[0] + .02])

        self.distribution = gaussian_kde(cat)

    '''
    Samples a point from this distribution between values a and b.
    '''
    def sample(self, a, b):
        assert a <= b

        lin = np.linspace(a, b, 100)

        # integrate using the trapezoidal method, returns all intermediate sums
        cumulated = cumtrapz(self.distribution(lin))

        if cumulated[-1] == 0:
            return b

        # normalize so the integral is equal to 1.0
        cumulated *= 1.0 / cumulated[-1]

        rand_val = random.random()

        index = np.nonzero(cumulated > rand_val)[0][0]
        return lin[index]
