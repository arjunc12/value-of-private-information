from population import *
from learner import *
from NPDistribution import *
import random

"""
This class describes a non-parametric distribution learning mechanism.

This mechanism essentially wraps a non-parametric distribution that is
modeled using a sum of Gaussians.

Additionally, this mechanism currently offers a payment draw from a
uniform distribution from the minimum cost to the maximum cost.

"""
class NPLearner(Learner):
    """
    Initialize this non-parametric distribution learning mechanism.

    num_types: number of distinct private types

    max_cost: maximum cost over all private types

    min_cost: minimum cost over all private types
    """
    def __init__(self, num_types, offer_strategy, max_cost, min_cost=0):
        self.min_cost = min_cost
        self.max_cost = max_cost
        self.num_types = num_types
        self.count = [1.0 for i in range(num_types)]
        self.distribution = [NPDistribution() for i in range(num_types)]
        for i in range(num_types):
          self.distribution[i].update(4, 1)
          self.distribution[i].update(6, 1)
        self.priv_type = []
        self.offer = []
        self.offer_strategy = offer_strategy


    """
    This should based on if the offer was accepted or not update
    the underlying non-parametric distrbutions correctly.
    """
    def update(self, priv_type, last_reject, offer):
        if priv_type == OFFER_REJECTED:
            self.update_reject(last_reject, offer)
        else:
            self.update_accept(priv_type, last_reject, offer)

        self.priv_type.append(priv_type)
        self.offer.append(offer)


    """
    This should update the underlying non-parmetric distrbutions
    given that the specified offer was rejected.

    last_reject: The last offer that was rejected,
                 None if there was no last rejection

    offer: The offer that was reject by the last person
    """
    def update_reject(self, last_reject, offer):
        weights = [self.count[i] * self.distribution[i].cdf(offer, self.max_cost)
                   for i in xrange(len(self.distribution))]
        overall_sum = (float)(sum(weights))
        for i in xrange(len(self.distribution)):
            self.distribution[i].update(self.distribution[i].sample(offer, self.max_cost),
                                        weights[i] / overall_sum)
            self.count[i] += weights[i] / overall_sum


    """
    This should update the underlying non-parametric distrbutions
    given that the specified offer was accepted and the
    individual was the specifed private type.

    priv_type: The private type of the individual that accepted

    last_reject: The last offer that was rejected,
                 None if there was no last rejection

    offer: The offer that was accepted by the individual
    """
    def update_accept(self, priv_type, last_reject, offer):
        self.count[priv_type] += 1
        dist = self.distribution[priv_type]
        if len(dist) != 0:
            dist.update(dist.sample(self.min_cost, offer), 1.0)
        else:
            dist.update(offer, 1.0)

    """
    This makes a random offer drawn from a uniform distrbution
    from the minimum cost to the maximum cost.

    returns: next offer to make
    """
    def make_offer(self):
        return self.offer_strategy(self)

    """
    Returns the predicted population.
    """
    def get_prediction(self):
        norm = sum(self.count)
        probability = [self.count[i] / norm for i in xrange(len(self.count))]
        return Population(probability, self.distribution)

