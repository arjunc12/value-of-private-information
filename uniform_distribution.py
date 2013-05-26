from distribution import *
import random
class UniformDistribution(Distribution):
  def __init__(self, start, end):
    self.start = start
    self.end = end
  def sample(self):
    return random.uniform(self.start, self.end)
  def __str__(self):
    return "UniformDistribution(start = " + str(self.start) + ", end = " + str(self.end) + ")"
    
