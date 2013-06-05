import random
import sys
import os
from datetime import datetime
import numpy
import cPickle as pickle
import matplotlib.pyplot as plt

from basic_learner import BasicLearner
from np_learner import NPLearner
import driver
from normal_distribution import NormalDistribution
from uniform_distribution import UniformDistribution
from utils import *
import offers

SEED = 3129412
MAX_OFFER = 15 # feel free to change this

"""
This file contains the code that runs the main experiment.
"""
def main():
    random.seed(SEED)
    numpy.random.seed(SEED)

    distribution = [
        (0.9, NormalDistribution(2, 1)),
        #(0.1, NormalDistribution(7, 1))
        (0.1, UniformDistribution(6.5, 7.5))
    ]

    args = sys.argv
    offer = offers.uniform_type_offer
    if '-offer' in args:
        i = args.index('-offer')
        offer_type = args[i + 1]

        if (offer_type == "random"):
            offer = offers.random_offer
        elif (offer_type == "max"):
            offer = offers.max_offer
        elif (offer_type == "uniform"):
            offer = offers.uniform_type_offer
        elif (offer_type == "most"):
            offer = offers.most_probable_type_offer
        elif (offer_type == "least"):
            offer = offers.least_probable_type_offer
        else:
            print "Offer strategy " + offer_type + " is not implemented."
            return

    ## Initialize a basic learner
    #learner = BasicLearner(len(distribution))

    # Initialize a non-parametric learner

    learner = NPLearner(len(distribution), offer, MAX_OFFER)

    init_offer = lambda l: offers.most_probable_type_offer(l).next()
    prob = lambda l: 0.5
    increment = lambda l: 1
    learner = NPLearner(len(distribution),
                        offers.configure_repeated_bidder(init_offer, prob, increment),
                        MAX_OFFER)

    # defaults
    constraint_type = driver.STEPS
    constraint_val = 1000


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
    prediction = results["prediction"]
    payout = results["spent"]
    individuals = results["individuals_seen"]
    divergences = results["divergences"]
    costs = results["costs"]
    #(prediction, payout, individuals, divergences) = results

    # little bit fragile
    accepted = sum(map(lambda x: len(x.definite_points), prediction.distribution))

    if '--save' in args:
        if not os.path.exists('data'):
            os.makedirs('data')
        fname = "data/run"
        format = "%Y-%m-%d-%H-%M-%S"
        path = "%s_%s_%s" % (fname, datetime.now().strftime(format), offer_type)
        f = open(path, 'w')
        pickle.dump((prediction, payout, individuals, divergences, costs), f)

    # Output information about the test
    print("population:\n" + str(d.population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(payout))
    print("accepted: " + str(accepted) + " / " + str(individuals))

    print joint_jsdivergence(d.population.distribution, prediction.distribution, d.population.probability, prediction.probability)
    plot_divergences(divergences)
    plot_costs(costs)

    for dist in prediction.distribution:
        plot_distribution(dist)


def plot_divergences(divergences):
    plt.plot(divergences)
    plt.title("js divergence over time")
    plt.xlabel("number of iterations")
    plt.ylabel("js-divergence")
    plt.ylim((0, 1))
    plt.show()

def plot_costs(costs):
    p1 = plt.plot(costs, label="learned costs")
    p2 = plt.plot(map(lambda x : x * MAX_OFFER, range(len(costs) + 1)), label="max cost")
    plt.legend()
    plt.title("cumulative cost over time")
    plt.xlabel("number of individuals seen")
    plt.ylabel("cumulative cost")
    plt.show()

if __name__ == "__main__":
    main()
