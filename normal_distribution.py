class NormalDistribution(Distribution):
  def __init__(self, mu, sigma):
    self.mu = mu
    self.sigma = sigma
  def sample(self):
    return random.gauss(mu, sigma)
    
