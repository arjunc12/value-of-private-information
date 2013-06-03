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
        if (learner.count[i] <= 20):
            enough = False
            break
    if (enough):
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
        if (learner.count[i] <= 20):
            enough = False
            break
    if (enough):
        offer = learner.get_prediction().sample()[1]
        yield offer
    else:
        yield random_offer(learner).next()
