from distribution import *
import random

"""
This class represents a normal distribution.
"""

class NormalDistribution(Distribution):
  """
  mu: mean of the distribution
  sigma: standard deviation of the distribution
  """
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma

  """
  Returns a random normally distributed variable.
  """
  def sample(self):
    return random.gauss(self.mu, self.sigma)

  """
  String that includes the mean and standard deviation of the Normal
  distribution.
  """
  def __str__(self):
    return "NormalDistribution(mu = " + str(self.mu) + ", sigma = " + str(self.sigma) + ")"

