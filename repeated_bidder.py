import random

class repeated_bidder:
    def __init__(self, p):
        """
        p is our baseline starting bid
        no matter how many offers we make, the expected value will always be
        p + epsilon
        """
        self.p = p
        self.eps = random.uniform(0, 1)
        self.alpha = [1]
        self.finished = False
        
    def current_offer(self):
        coefficient = reduce(lambda x y : x * y, self.alpha, 1)
        return (1.0 / coefficient) * (self.p + self.eps)
        
    def get_next_offer(self):
        if self.finished:
            return 0
            
        next_alpha = random.uniform(0, 1)
        p = random.uniform(0, 1)
        if p > next_alpha:
            self.finished = False
            return 0
        else
            self.alpha.append(next_alpha)
            return self.current_offer()
    