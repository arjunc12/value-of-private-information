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
        epsilon = 0.00001
        if pdf1 < epsilon and pdf2 < epsilon:
            return 0

        return math.log(pdf1 / pdf2) * pdf1

    return quad(klfunc, -numpy.inf, numpy.inf)

def jsdivergence(d1, d2):
    """
    takes two Distribution objects and computes js-divergence
    """
    def klfunc1(x):
        pdf1 = d1.pdf(x)
        pdf2 = d2.pdf(x)
        m = (pdf1 + pdf2) / 2

        # should definitely be 0 if pdf1 = 0
        # not sure how to handle case of pdf2 = 0 - for now returning 0
        epsilon = 0.00001
        if pdf1 < epsilon:
            return 0

        return math.log(pdf1 / m) * pdf1

    def klfunc2(x):
        pdf1 = d1.pdf(x)
        pdf2 = d2.pdf(x)
        m = (pdf1 + pdf2) / 2

        # should definitely be 0 if pdf1 = 0
        # not sure how to handle case of pdf2 = 0 - for now returning 0
        epsilon = 0.00001
        if pdf2 < epsilon:
            return 0

        return math.log(pdf2 / m) * pdf2

    return (quad(klfunc1, -numpy.inf, numpy.inf)[0] + quad(klfunc2, -numpy.inf, numpy.inf)[0]) / 2
