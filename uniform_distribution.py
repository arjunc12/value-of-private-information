class UniformDistribution(Distribution):
  def __init__(self, start, end):
    self.start = start
    self.end = end
  def sample(self):
    return random.uniform(start, end)
    
