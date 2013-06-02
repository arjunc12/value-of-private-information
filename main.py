from basic_learner import BasicLearner
from np_learner import NPLearner
import driver
from normal_distribution import NormalDistribution
from uniform_distribution import UniformDistribution

"""
This file contains the code that runs the main experiment.
"""
def main():
    distribution = [
        (0.9, NormalDistribution(1, 0.5)),
        (0.1, UniformDistribution(9, 10))
    ]

    ## Initialize a basic learner
    #learner = BasicLearner(len(distribution))

    # Initialize a non-parametric learner
    learner = NPLearner(len(distribution), 15)

    d = driver.Driver(distribution, driver.STEPS, 10000, learner)

    # Obtain the prediction population
    (prediction, payout, individuals) = d.run()

    # Output information about the test
    print("population:\n" + str(d.population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(payout))

if __name__ == "__main__":
    main()
