from scipy.integrate import quad
import numpy
import math

def kldivergence(d1, d2):
    """
    takes two Distribution objects and computes kl-divergence
    """
    def klfunc(x):
        pdf1 = d1.pdf(x)
        pdf2 = d2.pdf(x)
        # should definitely be 0 if pdf1 = 0
        # not sure how to handle case of pdf2 = 0 - for now returning 0
        if pdf1 == 0 or pdf2 == 0:
            return 0

        return math.log(pdf1 / pdf2) * pdf1

    return quad(klfunc, -numpy.inf, numpy.inf)[0]
