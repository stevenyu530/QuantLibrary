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
    from Cox-Ingersoll-Ross (1985). Euler Discretization approach is applied, for a full truncation

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
        paths_1 = np.zeros((num_dates, num_paths))
        paths_2 = np.zeros_like(paths_1)
        paths_1[0] = self.initial_value
        paths_2[0] = self.initial_value

        # decide the correct random numbers basted correlation
        if self.correlated is False:
            sn = sn_random_numbers((1, num_dates, num_paths), fixed_seed=fixed_seed)
        else:
            sn = self.random_numbers

        # Generate paths:
        for t in range(1, len(self.time_grid)):
            # time interval
            dt = (self.time_grid[t] - self.time_grid[t-1]).days / day_count

            # choose the correct random number
            if self.correlated is False:
                random_num = sn[t]
            else:
                random_num = np.dot(self.cholesky_matrix, sn[:, t, :])
                random_num = random_num[t]

            # full trunctation with Euler Discretization
            paths_2[t] = (paths_2[t-1] + self.kappa * (self.theta - np.maximum(0, paths_2[t-1, :])) * dt
                          + self.volatility * np.sqrt(np.maximum(0, paths_2[t-1, :])) * np.sqrt(dt) * random_num)
            paths_1[t] = np.maximum(0, paths_2[t])

        self.instrument_values = paths_1



