"""
This class is the abstract definition for a probability distribution.
"""

class Distribution(object):
    """
    Random sample from the probability distribution.
    """
    def sample(self):
        raise NotImplementedError()
        
    def pdf(self, x):
        raise NotImplementedError()
        
    def cdf(self, x):
        raise NotImplementedError()
        
    def inverseCDFIter(self, p, min=0, max=0):
        """
        uses binary search to iteratively calculate inverse cdf function
        if the upper and lower bounds on the distribution are known, the
        function can be called by passing these parameters
        """
        jump = 10
        while self.cdf(min) > p:
            min -= jump
            
        while self.cdf(max) < p:
            max += jump
            
        cutoff = 0.01        
        
        while True:
            x = 0.5 * (min + max)
            c = self.cdf(x)
            if abs(c - p) < cutoff:
                return x
            elif c < p:
                min = x
            else:
                max = x