from learner import OFFER_REJECTED
from population import Population
import utils

COST = 0
STEPS = 1

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

    def offer_process(self, cost):
        previous_offer = None
        for offer in self.learner.make_offer():
            if offer >= cost:
                return (True, previous_offer, offer)
            previous_offer = offer
        return (False, previous_offer, None)

    def run(self):
        if self.constraint_type == COST:
            return self.run_cost_constraint()
        elif self.constraint_type == STEPS:
            return self.run_steps_constraint()
        else:
            raise ValueError("Unknown constraint type")

    def run_cost_constraint(self):
        budget = self.constraint_val
        spent = 0.0
        individuals_seen = 0

        while spent < budget:
            # sample an individual from the population
            (priv_type, cost) = self.population.sample()

            accepted, rejected_offer, accepted_offer = self.offer_process(cost)
            if accepted:
                spent += accepted_offer
                ret_type = priv_type
            else:
                ret_type = OFFER_REJECTED

            self.learner.update(ret_type, rejected_offer, accepted_offer)
            individuals_seen += 1

        return (self.learner.get_prediction(), spent, individuals_seen)

    def run_steps_constraint(self):
        steps = self.constraint_val
        spent = 0.0

        for i in xrange(steps):
            # sample an individual from the population
            (priv_type, cost) = self.population.sample()

            accepted, rejected_offer, accepted_offer = self.offer_process(cost)
            if accepted:
                spent += accepted_offer
                ret_type = priv_type
            else:
                ret_type = OFFER_REJECTED

            self.learner.update(ret_type, rejected_offer, accepted_offer)

        return (self.learner.get_prediction(), spent, steps)
