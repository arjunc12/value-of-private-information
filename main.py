import random
import sys
import os
from datatime import datetime
from pickle import Pickler

from basic_learner import BasicLearner
from np_learner import NPLearner
import driver
from normal_distribution import NormalDistribution
from uniform_distribution import UniformDistribution
from offers import *

SEED = 3129412

"""
This file contains the code that runs the main experiment.
"""
def main():
    random.seed(SEED)

    distribution = [
        (0.9, NormalDistribution(1, 0.5)),
        (0.1, UniformDistribution(9, 10))
    ]

    ## Initialize a basic learner
    #learner = BasicLearner(len(distribution))

    # Initialize a non-parametric learner
    learner = NPLearner(len(distribution), uniform_type_offer, 15)
    
    constraint_type = driver.STEPS
    constraint_val = 1000
    args = sys.argv
    
    if '-c' in args:
        constraint_type = driver.COST
        i = args.index('-c')
        constraint_val = float(args[i + 1])
    elif '-s' in args:
        i = args.index('-s')
        constraint_val = float(args[i + 1])
     
    d = driver.Driver(distribution, constraint_type, constraint_val, learner)
    
    # Obtain the prediction population
    (prediction, payout, individuals) = d.run()
    
    if '--save' in args:
        if not os.path.exists('data'):
            os.makedirs('data')
        f = open(str(datetime.now()) + '.dat', 'w')
        p.dump(f, (distribution, constraint_type, constraint_val, learner, prediction, payout, individuals))
    

    # Output information about the test
    print("population:\n" + str(d.population))
    print("prediction:\n" + str(prediction))
    print("total_payout: " + str(payout))
    print("accepted: " + str(accepted) + " / " + str(individuals))

if __name__ == "__main__":
    main()
