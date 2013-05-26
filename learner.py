"""
This class is the abstract definition for a learning mechanism.
"""

# TODO: How to make this abstract?
class Learner:
  """
  Constructor for the learning mechanism.
  """
  def __init__(self):
    pass

  """
  update will be called repeatedly by the main loop. Each call explains the
  result of the previous query and expects an offer for the next payout.

  priv_type: private type of the previous query
             -2: first query, no previous query to report
             -1: previous offer rejected
             0 - ???: private type of the previous query (offer accepted)

  Returns an offer for the next payout.
  """
  def update(self, priv_type):
    pass

  """
  Returns the predicted Population.
  """
  def get_prediction(self):
    pass

