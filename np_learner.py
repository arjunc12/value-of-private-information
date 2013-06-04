from population import *
from learner import *
from NPDistribution import *
import random
from types import MethodType

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

    offer_strategy: A valid generator function that generates values greater than 0
    """
    def __init__(self, num_types, offer_strategy, max_cost, min_cost=0):
        self.min_cost = min_cost
        self.max_cost = max_cost
        self.num_types = num_types
        self.count = [1.0 for i in range(num_types)]
        self.distribution = [NPDistribution() for i in range(num_types)]
        self.priv_type = []
        self.offer = []

        self.make_offer = MethodType(offer_strategy, self)


    """
    This should based on if the offer was accepted or not update
    the underlying non-parametric distrbutions correctly.
    """
    def update(self, priv_type, rejected_offer, accepted_offer):
        if priv_type == OFFER_REJECTED:
            self.update_reject(rejected_offer)
        else:
            self.update_accept(priv_type, rejected_offer, accepted_offer)

        self.priv_type.append(priv_type)
        self.offer.append(accepted_offer)


    """
    This should update the underlying non-parametric distrbutions
    given that the specified offer was rejected.

    offer: The offer that was reject by the last person
    """
    def update_reject(self, offer):
        weights = [self.count[i] * self.distribution[i].cdf(offer, self.max_cost)
                   for i in xrange(len(self.distribution))]

        overall_sum = float(sum(weights))

        for i in xrange(len(self.distribution)):
            if len(self.distribution[i]) != 0:
                sample = self.distribution[i].sample(offer, self.max_cost)
                self.distribution[i].update(sample, weights[i] / overall_sum)
                self.count[i] += weights[i] / overall_sum


    """
    This should update the underlying non-parametric distrbutions
    given that the specified offer was accepted and the
    individual was the specifed private type.

    priv_type: The private type of the individual that accepted

    rejected_offer: The last offer that was rejected,
                 None if there was no last rejection

    accepted_offer: The offer that was accepted by the individual
    """
    def update_accept(self, priv_type, rejected_offer, accepted_offer):
        self.count[priv_type] += 1
        dist = self.distribution[priv_type]
        dist.update(dist.sample(self.min_cost, accepted_offer), 1.0)

    """
    Returns the predicted population.
    """
    def get_prediction(self):
        norm = sum(self.count)
        probability = [self.count[i] / norm for i in xrange(len(self.count))]
        return Population(probability, self.distribution)
