#
# Random number generation is a central task of Monte Carlo simulation.
# A standard normally distributed random numbers generator is implemented in this function
# with several variance reduction techniques
#

import numpy as np

def sn_random_numbers(shape, antithetic=True, moment_matching=True, fixed_seed=False):
    '''
    Returns an array of shape with (pseudo) random numbers, that are standard normally distributed

    :param shape: tuple(o, n, m)
        generation of array with shape (o,n,m)
    :param antithetic: Boolean
        setting for antithetic variates
    :param moment_matching: Boolean
        matching of first and second moments
    :param fixed_seed: Boolean
        flag to fix the seed

    :return: random(o,n,m) array of pseudo random numbers
    '''

    if fixed_seed:
        np.random.seed(1000)

    if antithetic:
        random = np.random.standard_normal((shape[0], shape[1], shape[2]/2))
        random = np.concatenate((random, -random), axis=2)
    else:
        random = np.random.standard_normal(shape)

    if moment_matching:
        random = random - np.mean(random)
        random = random / np.std(random)

    if shape[0] ==  1:
        return random[0]
    else:
        return random