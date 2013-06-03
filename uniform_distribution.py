from distribution import *
import random

"""
This class represents a uniform distribution.
"""

class UniformDistribution(Distribution):
    """
    start: lower end of the uniform distribution
    end: upper end of the uniform distribution
    Note: start <= end
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    """
    Returns a random uniformly distributed variable.
    """
    def sample(self):
        return random.uniform(self.start, self.end)

    """
    String that includes the lower and upper bounds of the uniform distribution.
    """
    def __str__(self):
        return "UniformDistribution(start = " + str(self.start) + ", end = " + str(self.end) + ")"
        
    def pdf(self, x):
        if x < self.start or x >= self.end:
            return 0
        return 1.0 / (self.end - self.start)
        
    def cdf(self, x):
        if x < self.start:
            return 0
        elif x > self.end:
            return 1
        else:
            return float(x - self.start) / float(self.end - self.start)
