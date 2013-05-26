from distribution import *
import random
class NormalDistribution(Distribution):
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma
  def sample(self):
    return random.gauss(self.mu, self.sigma)
  def __str__(self):
    return "NormalDistribution(mu = " + str(self.mu) + ", sigma = " + str(self.sigma) + ")"
    
