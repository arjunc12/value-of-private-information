from population import *
from normal_distribution import *
from uniform_distribution import *
from learner import *
from basic_learner import *

"""
This file contains the code that runs the main experiment.
"""
def main():
    learner = BasicLearner(2) # Initialize a basic learner (2 private types)
    probability = [0.9, 0.1] # Probability that each private type appears
    # Distribution of cost distributions for each private type
    distribution = [NormalDistribution(1, 0.5), UniformDistribution(9, 10)]
    population = Population(probability, distribution) # Initialize the population

    total_payout = 0 # Total payout made by the mechanism (sum of accepted offers)
    priv_type = -2 # Private type of previous offer (-2: first offer, special case)
    for i in range(1000):
        payout = learner.update(priv_type) # Report previous result, obtain new offer
        [priv_type, value] = population.sample() # Obtain random person
        if (value <= payout): # Offer accepted
            total_payout += payout # Required to pay
        else: # Offer rejected
            priv_type = -1 # no information reported

    payout = learner.update(priv_type) # Send the result of the last offer

    prediction = learner.get_prediction() # Obtain the predicted population

    # Output information about the test
    print("population:\n" + str(population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(total_payout))

if __name__ == "__main__":
    main()
