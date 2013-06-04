import random
from np_learner import NPLearner

def random_offer(learner):
    """
    Returns a random offer uniformly drawn from min to max.
    """
    yield random.uniform(learner.min_cost, learner.max_cost)

def uniform_type_offer(learner):
    """
    Returns an offer designed to uniformly sample the population
    """
    enough = True
    for i in range(len(learner.count)):
        if learner.count[i] <= 20:
            enough = False
            break
    if enough:
        offer = learner.distribution[random.randint(0, len(learner.count) - 1)].sample()
        yield offer
    else:
        yield random_offer(learner).next()


def most_probable_type_offer(learner):
    """
    Returns an offer designed to sample the population for the most common private type.
    """
    enough = True
    for i in range(len(learner.count)):
        if learner.count[i] <= 20:
            enough = False
            break
    if enough:
        offer = learner.get_prediction().sample()[1]
        yield offer
    else:
        yield random_offer(learner).next()

def least_probable_type_offer(learner):
    """
    Returns an offer designed to sample the population for the least common private type.
    """
    enough = True
    for i in range(len(learner.count)):
        if learner.count[i] <= 20:
            enough = False
            break
    if enough:
        # Find the distribution with the least cost
        scores = [len(distr.definite_points) +
                  sum(map(lambda x: x[1], distr.possible_points))
                  for distr in learner.distribution]
        index = scores.index(min(scores))
        max_cost = max(learner.distribution[index].definite_points)
        min_cost = min(learner.distribution[index].definite_points)
        offer = learner.distribution[index].sample(min_cost, max_cost)
        yield offer
    else:
        yield random_offer(learner).next()

'''
Initial_offer, probability, and increment are all functions of learner.
Probability is probability of making another offer.
'''
def configure_repeated_bidder(initial_offer, probability, increment):
    def inner(learner):
        prob = probability(learner)
        inc = increment(learner)
        offer = initial_offer(learner)

        yield offer
        while random.random() < prob:
            offer += inc
            yield offer

    return inner
