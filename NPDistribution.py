import random

import numpy as np
from scipy.integrate import cumtrapz
from scipy.stats import gaussian_kde

from distribution import Distribution

# zomg so arbitrary
OFFSET = 10

class NPDistribution(Distribution):
    def __init__(self):
        self.definite_points = []
        self.possible_points = []
        self.distribution = None

    def __len__(self):
        return len(self.definite_points)

    '''
    Returns the probability mass under x
    '''
    def pdf(self, x):
        return self.distribution([x])[0]

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
            mask = a[:, 1] > np.random.rand(len(self.possible_points))
            sampled = a[:, 0][mask]

            points = np.concatenate(np.array(self.definite_points), sampled)
        else:
            points = np.array(self.definite_points)

        if points.size > 1:
            self.distribution = gaussian_kde(points)
        else:
            # THIS IS AN UGLY HACK
            points = np.array([points[0] - OFFSET, points[0] + OFFSET])
            # bw_method?
            self.distribution = gaussian_kde(points)

    '''
    Samples a point from this distribution between values a and b.
    '''
    def sample(self, a, b):
        assert a <= b

        lin = np.linspace(a, b, 100)

        # integrate using the trapezoidal method, returns all intermediate sums
        cumulated = cumtrapz(self.distribution(lin))

        # no probability mass, just return the average
        if cumulated[-1] == 0:
            return (a + b) / 2.0

        # normalize so the integral is equal to 1.0
        cumulated *= 1.0 / cumulated[-1]

        rand_val = random.random()

        index = np.nonzero(cumulated > rand_val)[0][0]
        return lin[index]
