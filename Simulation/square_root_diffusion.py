#
# Author: Steven YU
# QuantLibrary Simulation
# square_root_diffusion.py
# #

import numpy as np

from sn_random_numbers import sn_random_numbers
from simulation_class import simulation_class

class square_root_diffusion(simulation_class):
    """
    Class to genreate simulated paths based on the Square-Root Diffusion model
    from Cox-Ingersoll-Ross (1985). Euler Discretization approach is applied

    Attributes:
    ===========
    name: string
        name of the object
    mkt_env: market_environment
        market environment parameter data for simulation
    correlated : Boolean
        decide if the object is correlated with other model object

    Methods:
    ========
    update :
        update parameters
    generate_paths:
        returns Monte Carlo simulated paths based on the market parameters
    """

    def __init__(self, name, mkt_env, correlated=False):
        super(square_root_diffusion, self).__init__(name, mkt_env, correlated)
        try:
            self.kappa = mkt_env.get_constant('kappa')
            self.theta = mkt_env.get_constant('theta')
        except:
            print "Error parsing market environment parameters"

    def update (self, initial_value=None, volatility=None, kappa=None,
                theta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if kappa is not None:
            self.kappa = kappa
        if theta is not None:
            self.theta = theta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=True, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()

        num_dates = len(self.time_grid)
        num_paths = self.paths
        paths = np.zeros((num_dates, num_paths))
        paths[0] = self.initial_value

        # decide the correct random numbers basted correlation
        if self.correlated:
            sn_random_numbers = sn_random_numbers((1, num_dates, num_paths), fixed_seed=fixed_seed)
        else:
            sn_random_numbers = self.random_numbers

        # Generate paths

