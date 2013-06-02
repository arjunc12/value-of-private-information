from learner import *
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
    def __init__(self, num_types, max_cost, min_cost=0):
        #raise NotImplementedError()
        self.num_types = num_types # number of distinct private types
        self.total = 0 # total number of accepted payout offers
        self.count = num_types * [0] # count of accepted offers from each type
        self.lower = num_types * [float("+inf")] # smallest accepted offer from each type
        self.upper = num_types * [0] # largest accepted offer from each type
        self.payout = 0 # next payout offer to be made
        self.max = max_cost
        self.min = min_cost


    """
    This should based on if the offer was accepted or not update
    the underlying non-parametric distrbutions correctly.
    """
    def update(self, priv_type, offer):
        raise NotImplementedError()


    """
    This should update the underlying non-parmetric distrbutions
    given that the specified offer was rejected.

    offer: The offer that was reject by the last person
    """
    def update_reject(self, offer):
        raise NotImplementedError()


    """
    This should update the underlying non-parametric distrbutions
    given that the specified offer was accepted and the
    individual was the specifed private type.

    priv_type: The private type of the individual that accepted

    offer: The offer that was accepted by the individual
    """
    def update_accept(self, priv_type, offer):
        #raise NotImplementedError()
        self.total += 1
        self.count[priv_type] += 1
        if offer < self.lower[priv_type]:
            self.lower[priv_type] = offer
        if offer > self.upper[priv_type]:
            self.upper[priv_type] = offer
        
    """
    This makes a random offer drawn from a uniform distrbution
    from the minimum cost to the maximum cost.

    returns: next offer to make
    """
    def make_offer(self):
        #raise NotImplementedError()
        return random.uniform(self.min, self.max)

    """
    Returns the predicted population.
    """
    def get_prediction(self):
        raise NotImplementedError()
