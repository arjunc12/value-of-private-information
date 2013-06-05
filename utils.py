from scipy.integrate import quad
import numpy
import math
import matplotlib.pyplot as plt

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
        if pdf1 < epsilon:
            return 0

        return math.log(pdf1 / pdf2) * pdf1

    return quad(klfunc, -numpy.inf, numpy.inf)[0]

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

def joint_jsdivergence(dist1, dist2, prob1, prob2):
    """
    takes two Distribution objects and computes js-divergence
    """
    def klfunc(x):
        pdf1 = p1 * d1.pdf(x)
        pdf2 = p2 * d2.pdf(x)
        m = (pdf1 + pdf2) / 2

        # should definitely be 0 if pdf1 = 0
        # not sure how to handle case of pdf2 = 0 - for now returning 0
        epsilon = 0.00001
        if pdf1 < epsilon:
            return 0

        return math.log(pdf1 / m) * pdf1

    ans = 0.0
    for i in xrange(len(dist1)):
        d1 = dist1[i]
        d2 = dist2[i]
        p1 = prob1[i]
        p2 = prob2[i]
        ans += quad(klfunc, -numpy.inf, numpy.inf)[0] / 2

        d1 = dist2[i]
        d2 = dist1[i]
        p1 = prob2[i]
        p2 = prob1[i]
        ans += quad(klfunc, -numpy.inf, numpy.inf)[0] / 2
    return ans

def plot_distribution(dist, leftend=-10, rightend=10, step=0.2):
    x = numpy.arange(leftend, rightend, step)
    y = map(dist.pdf, x)
    plt.plot(x, y)
    plt.show()