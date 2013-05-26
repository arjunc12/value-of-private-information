from learner import *
from uniform_distribution import *
from population import *
class BasicLearner(Learner):
  def __init__(self, num_types):
    self.num_types = num_types
    self.total = 0
    self.count = num_types * [0]
    self.lower = num_types * [float("+inf")]
    self.upper = num_types * [0]
    self.payout = 0

  def update(self, priv_type):
    if (priv_type >= 0):
      self.total += 1
      self.count[priv_type] += 1
      self.lower[priv_type] = min(self.lower[priv_type], self.payout)
      self.upper[priv_type] = max(self.upper[priv_type], self.payout)
    elif (priv_type == -1):
      self.payout += 0.1
    return self.payout

  def get_prediction(self):
    probability = self.num_types * [0]
    distribution = self.num_types * [0]
    for i in range(self.num_types):
      probability[i] = self.count[i] / float(self.total)
      distribution[i] = UniformDistribution(self.lower[i], self.upper[i])

    return Population(probability, distribution)
