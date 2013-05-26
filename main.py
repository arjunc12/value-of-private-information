from population import *
from normal_distribution import *
from uniform_distribution import *
from learner import *
from basic_learner import *
def main():
  learner = BasicLearner(2);
  population = Population([0.9, 0.1], [NormalDistribution(1, 0.5), UniformDistribution(9, 10)])

  total_payout = 0
  priv_type = -2
  for i in range(1000):
    payout = learner.update(priv_type)
    [priv_type, value] = population.sample()
    if (value <= payout):
      total_payout += payout
    else:
      priv_type = -1

  payout = learner.update(priv_type)

  prediction = learner.get_prediction()

  print("population:\n" + str(population))
  print("prediction:\n" + str(prediction))
  print("total_payout: " + str(total_payout))

if __name__ == "__main__":
    main()
