"""
This class is the abstract definition for a probability distribution.
"""

class Distribution(object):
    """
    Random sample from the probability distribution.
    """
    def sample(self):
        raise NotImplementedError()
