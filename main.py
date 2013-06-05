import random
import sys
import os
from datetime import datetime
import numpy
import pickle
import matplotlib.pyplot as plt

from basic_learner import BasicLearner
from np_learner import NPLearner
import driver
from normal_distribution import NormalDistribution
from uniform_distribution import UniformDistribution
import offers

SEED = 3129412

"""
This file contains the code that runs the main experiment.
"""
def main():
    random.seed(SEED)
    numpy.random.seed(SEED)

    distribution = [
        (0.9, NormalDistribution(1, 0.5)),
        (0.1, UniformDistribution(9, 10))
    ]

    ## Initialize a basic learner
    #learner = BasicLearner(len(distribution))

    # Initialize a non-parametric learner

    #learner = NPLearner(len(distribution), offers.uniform_type_offer, 15)

    init_offer = lambda l: offers.most_probable_type_offer(l).next()
    prob = lambda l: 0.5
    increment = lambda l: 1
    learner = NPLearner(len(distribution),
                        offers.configure_repeated_bidder(init_offer, prob, increment),
                        15)

    # defaults
    constraint_type = driver.STEPS
    constraint_val = 1000

    args = sys.argv

    if '-c' in args:
        constraint_type = driver.COST
        i = args.index('-c')
        constraint_val = float(args[i + 1])
    elif '-s' in args:
        i = args.index('-s')
        constraint_val = int(args[i + 1])
    elif '-b' in args:
        constraint_type = driver.BASELINE
        i = args.index('-b')
        constraint_val = int(args[i + 1])

    d = driver.Driver(distribution, constraint_type, constraint_val, learner)

    # Obtain the prediction population
    results = d.run()
    (prediction, payout, individuals, divergences) = results

    # little bit fragile
    accepted = sum(map(lambda x: len(x.definite_points), prediction.distribution))

    if '--save' in args:
        if not os.path.exists('data'):
            os.makedirs('data')
        fname = "data/run"
        format = "%Y-%m-%d-%H-%M-%S"
        path = "%s_%s" % (fname, datetime.now().strftime(format))
        f = open(path, 'w')
        pickle.dump( result + (prediction, payout, individuals), f)

    # Output information about the test
    print("population:\n" + str(d.population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(payout))
    print("accepted: " + str(accepted) + " / " + str(individuals))
    plot_divergences(divergences)

def plot_divergences(divergences):
    plt.plot(divergences)
    plt.title("js divergence over time")
    plt.xlabel("number of iterations")
    plt.ylabel("js-divergence")
    plt.ylim((0, 1))
    plt.show()

if __name__ == "__main__":
    main()
