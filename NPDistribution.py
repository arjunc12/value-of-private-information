import random

import numpy as np
from scipy.integrate import cumtrapz
from scipy.stats import gaussian_kde

from distribution import Distribution

# zomg so arbitrary
OFFSET = 3

PRIOR = gaussian_kde([4, 6])

class NPDistribution(Distribution):
    def __init__(self):
        self.definite_points = []
        self.possible_points = []
        self.distribution = PRIOR

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
    def cdf(self, a, b=None):
        if (b != None):
            return self.distribution.integrate_box_1d(a, b)
        return self.distribution.integrate_box_1d(0, a)

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

        # just keep the PRIOR distribution
        if self.definite_points == []:
            return

        if self.possible_points != []:
            # turn into an array for numpy's purposes
            a = np.array(self.possible_points)

            # want to keep if weight is greater than random number
            mask = a[:, 1] > np.random.rand(len(self.possible_points))
            sampled = a[:, 0][mask]

            if (sampled != []):
                points = np.concatenate((np.array(self.definite_points), np.array(sampled)))
            else:
                points = np.array(self.definite_points)
        else:
            points = np.array(self.definite_points)

        if points.size > 1:
            self.distribution = gaussian_kde(points)
        else:
            # THIS IS AN UGLY HACK, need 2 pts initially
            points = np.array([points[0] - OFFSET, points[0] + OFFSET])
            self.distribution = gaussian_kde(points)

    '''
    Samples a point from this distribution between values a and b.
    '''
    def sample(self, a=0, b=100):
        assert a <= b

        lin = np.linspace(a, b, 1000)

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

    """
    Returns a string representing the distribution.
    """
    def __str__(self):
        return "NPDistribution([" + str(self.inverseCDFIter(0.25)) + ", " + str(self.inverseCDFIter(0.50)) + ", " + str(self.inverseCDFIter(0.75)) + "])"
