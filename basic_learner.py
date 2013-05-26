from learner import *
from uniform_distribution import *
from population import *

"""
This class describes a simple learning mechanism.

The mechanism only requires the number of distinct private types to be
initizlized.

The mechanism will initially offer payouts of 0 and increase the payout by
0.1 every time an offer is rejected.

To compute the probability of each private type appearing, only the frequency
of appearance in accepted offers is considered (which can be fairly
unreliable). The cost distributions for all private types is assumed to be
uniform. The lower bound of the distribution is the smallest accepted offer
from that type, and the upper bound of the distribution is the largest
accepted offer from that type (rejected offers are completely ignored, and
the distribution for a type that is entirely unsampled is nonsense).
"""
class BasicLearner(Learner):
  """
  num_types: number of distinct private types
  """
  def __init__(self, num_types):
    self.num_types = num_types # number of distinct private types
    self.total = 0 # total number of accepted payout offers
    self.count = num_types * [0] # count of accepted offers from each type
    self.lower = num_types * [float("+inf")] # smallest accepted offer from each type
    self.upper = num_types * [0] # largest accepted offer from each type
    self.payout = 0 # next payout offer to be made

  def update(self, priv_type):
    if (priv_type >= 0): # last offer was accepted
      self.total += 1 # one more accepted offer
      self.count[priv_type] += 1 # one more accepted offer for the type
      self.lower[priv_type] = min(self.lower[priv_type], self.payout) # update lowest accepted offer from type
      self.upper[priv_type] = max(self.upper[priv_type], self.payout) # update highest accepted offer from type
    elif (priv_type == -1): # last offer rejected
      self.payout += 0.1 # increase next payout

    return self.payout # give offer for next payout

  """
  This function returns the predicted population.
  """
  def get_prediction(self):
    probability = self.num_types * [0]
    distribution = self.num_types * [0]
    for i in range(self.num_types):
      probability[i] = self.count[i] / float(self.total)
      distribution[i] = UniformDistribution(self.lower[i], self.upper[i])

    return Population(probability, distribution)

