class Population:
  def __init__(self, probability, distribution):
    self.probability = probability
    self.distribution = distribution
    self.num_types = size(probability)
  def sample(self):
    p = random.random()
    priv_type = -1
    cum_sum = 0
    for i in range(self.num_types):
      cum_sum += self.probability[i]
      if (p < cum_sum):
        priv_type = i
        break

    value = distribution[i].sample

    return (priv_type, value)


