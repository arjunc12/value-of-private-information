"""
This class is the abstract definition for a learning mechanism.
"""

FIRST_OFFER = -2
OFFER_REJECTED = -1

class Learner(object):
    """
    update will be called repeatedly by the main loop. Each call explains the
    result of the previous query and expects an offer for the next payout.

    priv_type: private type of the previous query
                         FIRST_OFFER: first query, no previous query to report
                         OFFER_REJECTED: previous offer rejected
                         priv_type >= 0 : private type of the previous query (offer accepted)

    Returns an offer for the next payout.
    """
    def update(self, priv_type):
        raise NotImplementedError()

    """
    Returns the predicted Population.
    """
    def get_prediction(self):
        raise NotImplementedError()
