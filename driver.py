from learner import OFFER_REJECTED
from population import Population
import utils
from collections import defaultdict
from NPDistribution import *

COST = 0
STEPS = 1
BASELINE = 2

class Driver(object):
    '''
    Parameters:

    population_distribution:
      A list of 2-tuples. There is a 2-tuple for each private type. The first
      element of the 2-tuple is how often that type occurs in the full
      population (ie a number 0<=x<=1, all of these numbers sum to 1). The
      second item in each 2-tuple is a Distribution object that represents the
      cost distribution of that type.

    constraint_type:
      Are we constrained by how many individuals we are going to talk to (ie how
      many steps we are going to run the loop) or how much money we are going to
      spend? Use the values defined above (COST or STEPS) to specify this
      parameter.

    constaint_val:
      Interpretation depends on constraint_type. Either how many steps we are
      going to run or how much money we are willing to spend (aka the budget).

    learner: A Learner object.
    '''
    def __init__(self,
                 population_distribution,
                 constraint_type,
                 constraint_val,
                 learner):

        # initialize population
        self.population = Population(*zip(*population_distribution))

        self.constraint_type = constraint_type
        self.constraint_val = constraint_val
        self.learner = learner
        # dic mapping each type to the list of kl divergences over time
        self.costs = [0]
        self.divergences = []

        # dictionary that will contain everything we want to return at the end
        # if you have a new thing you want to return, just add it to the
        # dictionary instead of changing the tuple size
        self.results = {}
        self.results["population"] = self.population
        self.results["constraint_type"] = self.constraint_type
        self.results["constraint_val"] = self.constraint_val
        self.results["learner"] = self.learner
        self.results["costs"] = self.costs
        self.results["divergences"] = self.divergences

    '''
    This function allows us to interactively haggle with someone's data that
    we want to buy. The 'cost' parameter is the value that the individual attaches
    to keeping their data private.
    The return value of this function is a 3 tuple: (accepted, rejected_offer, accepted_offer)

    'accepted' is a boolean of whether or not the individual accepted an offer.
    'rejected_offer' is the greatest value of any offer the individual rejected.
    'accepted_offer' is the value of the offer that the user accepted.

    Note that either 'accepted_offer' will be None when accepted is False, and that
    'rejected_offer' can be None when accepted_offer is True (if they accepted the first offer).
    '''
    def offer_process(self, cost):
        previous_offer = None
        for offer in self.learner.make_offer():
            if offer >= cost:
                return (True, previous_offer, offer)
            previous_offer = offer
        return (False, previous_offer, None)

    '''
    The main function of this class. Returns a 3-tuple: (distribution, spent, individuals_seen)
    'distribution' is a population object representing what we learned about each type.
    'spent' is how much money we paid out, 'individuals_seen' is how many individuals we talked to.
    '''
    def run(self):
        if self.constraint_type == COST:
            return self.run_cost_constraint()
        elif self.constraint_type == STEPS:
            return self.run_steps_constraint()
        elif self.constraint_type == BASELINE:
            return self.run_baseline()
        else:
            raise ValueError("Unknown constraint type")

    def get_distribution_for_type(self, priv_type):
        return self.population.distribution[priv_type]

    def update_costs(self, cost):
        self.costs.append(cost)


    def update_divergences(self, learned_pop):
        js_div = utils.joint_jsdivergence(self.population.distribution, learned_pop.distribution, self.population.probability, learned_pop.probability)
        self.divergences.append(js_div)

    def run_cost_constraint(self):
        budget = self.constraint_val
        spent = 0.0
        individuals_seen = 0

        count = [0 for i in range(self.population.num_types)]
        while spent < budget:
            # sample an individual from the population
            (priv_type, cost) = self.population.sample()
            count[priv_type] += 1

            accepted, rejected_offer, accepted_offer = self.offer_process(cost)
            if accepted:
                print "Offer #" + str(i) + ":\t" + str(rejected_offer) + " Rejected\t" + str(accepted_offer) + " Accepted"
                spent += accepted_offer
                ret_type = priv_type
            else:
                print "Offer #" + str(i) + ":\t" + str(rejected_offer) + " Rejected"
                ret_type = OFFER_REJECTED

            self.learner.update(ret_type, rejected_offer, accepted_offer)
            individuals_seen += 1

            self.update_costs(spent)
            learned_pop = self.learner.get_prediction()
            self.update_divergences(learned_pop)

        #return (self.learner.get_prediction(), spent, individuals_seen, self.divergences)
        self.results["prediction"] = self.learner.get_prediction()
        self.results["spent"] = spent
        self.results["individuals_seen"] = individuals_seen
        return self.results

    def run_steps_constraint(self):
        steps = self.constraint_val
        spent = 0.0
        count = [0 for i in range(self.population.num_types)]

        for i in xrange(steps):
            # sample an individual from the population
            (priv_type, cost) = self.population.sample()
            count[priv_type] += 1

            accepted, rejected_offer, accepted_offer = self.offer_process(cost)
            if accepted:
                print "Offer #" + str(i) + ":\t" + str(rejected_offer) + " Rejected\t" + str(accepted_offer) + " Accepted"
                spent += accepted_offer
                ret_type = priv_type
            else:
                print "Offer #" + str(i) + ":\t" + str(rejected_offer) + " Rejected"
                ret_type = OFFER_REJECTED

            self.learner.update(ret_type, rejected_offer, accepted_offer)
            # compute new kl-divergence
            self.update_costs(spent)

            learned_pop = self.learner.get_prediction()
            self.update_divergences(learned_pop)

        #return (self.learner.get_prediction(), spent, steps, self.divergences)
        self.results["prediction"] = self.learner.get_prediction()
        self.results["spent"] = spent
        self.results["individuals_seen"] = steps
        return self.results

    def run_baseline(self):
        steps = self.constraint_val
        spent = 0.0
        count = [0 for i in range(self.population.num_types)]
        distribution = [NPDistribution() for i in range(self.population.num_types)]

        for i in xrange(steps):
            print "Offer #" + str(i) + " / " + str(steps)
            # sample an individual from the population
            (priv_type, cost) = self.population.sample()
            count[priv_type] += 1
            distribution[priv_type].update(cost, 1)
            spent += cost

            self.update_costs(spent)
            # compute new kl-divergence
            prob = [None for j in xrange(self.population.num_types)]
            for j in xrange(self.population.num_types):
                prob[j] = count[j] / float(sum(count))

            learned_pop = Population(prob, distribution)
            self.update_divergences(learned_pop)
        #return (learned_pop, spent, steps, self.divergences)
        self.results["prediction"] = learned_pop
        self.results["spent"] = spent
        self.results["individuals_seen"] = steps
        return self.results
