"""
This class is the abstract definition for a learning mechanism.
"""

OFFER_REJECTED = -1

class Learner(object):
    """
    update will be called repeatedly by the main loop. Each call explains the
    result of the previous query and expects an offer for the next payout.

    priv_type: private type of the previous query
                         FIRST_OFFER: first query, no previous query to report
                         OFFER_REJECTED: previous offer rejected
                         priv_type >= 0 : private type of the previous query (offer accepted)


    offer: How much did we offer the last person?

    Doesn't need to return anything
    """
    def update(self, priv_type, offer):
        raise NotImplementedError()

    '''
    Returns how much we should offer the next individual.
    '''
    def make_offer(self):
        raise NotImplementedError()

    """
    Returns the predicted Population.
    """
    def get_prediction(self):
        raise NotImplementedError()
        
    def __str__(self):
        return "learner"
