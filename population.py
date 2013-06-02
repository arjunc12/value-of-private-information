"""
This class contains the information for a group of different private types.
Each private type appears with a certain probability, and each private type
has a distribution for its cost function.
"""

import random

class Population(object):
    """
    probability: list of floating point numbers that sum (approximately) to 1
                             represent the probability that each private type appears
    distribution: list of Distributions
                                represent the distribution of cost functions
    Note: The lengths of probability and distribution must be equal.
    """
    def __init__(self, probability, distribution):
        self.probability = probability
        self.distribution = distribution
        self.num_types = len(probability)

    """
    Returns a 2-tuple that consists of the (1) private type and (2) value for
    privacy of a random individual from the population.
    """
    def sample(self):
        p = random.random()
        priv_type = -1
        cum_sum = 0
        for i in range(self.num_types):
            cum_sum += self.probability[i]
            if (p < cum_sum):
                priv_type = i
                break

        value = self.distribution[i].sample()

        return (priv_type, value)

    """
    Returns a string that represents the population.
    The string consists of the distributions and probabilities of the different
    private types
    """
    def __str__(self):
        string = ""
        for i in range(self.num_types):
            string += (str(self.distribution[i]) + ":\t" + str(self.probability[i]) + "\n")
        return string
