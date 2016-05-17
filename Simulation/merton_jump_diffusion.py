#
# QuantLibrary Simulation
# merton_jump_diffusion.py
#
import numpy as np

from sn_random_numbers import sn_random_numbers
from simulation_class import simulation_class

class merton_jump_diffusion(simulation_class):
    """
    Class to generate simulated paths based on Merton Jump Diffusion model (1976)

    Attributes:
    ===========
    name : string
        name of the object
    mkt_env : instance of market_environment
        market environment data for simulation
    correlated : Boolean
        decide if the object is correlated with other model object

    Methods:
    ========
    update :
        update parameters
    generate_paths:
        returns Monte Carlo paths based on the market parameters
    """

    def __init__(self, name, mkt_env, correlated=False):
        super(merton_jump_diffusion, self).__init__(name, mkt_env, correlated)
        try:
            # additional parameters
            self.lamb = mkt_env.get_constant('lambda')
            self.mu = mkt_env.get_constant('mu')
            self.delta = mkt_env.get_constant('delta')
        except:
            print "Error parsing market environment"


    def update (self, initial_value=None, volatility=None, lamb=None,
                mu=None, delta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if lamb is not None:
            self.lamb = lamb
        if mu is not None:
            self.mu = mu
        if delta is not None:
            self.delta = delta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None


    def generate_paths(self, fixed_seed=False, day_count=365.):
        # prepare time grids
        if self.time_grid is None:
            self.generate_time_grid()

        num_dates = len(self.time_grid)
        num_paths = self.paths
        paths = np.zeros((num_dates, num_paths))
        paths[0] = self.initial_value   # set starting value on the first date to be the initial value

        if self.correlated is False:
            # if not correlated with other models, generate Standard Normal Distributed random numbers
            sn1 = sn_random_numbers((1, num_dates, num_paths), fixed_seed=fixed_seed)
        else:
            # if correlated, use random number as provided in market environment
            sn1 = self.random_numbers

        # Standard Normally Distributed random numbers
        # in the jump component
        sn2 = sn_random_numbers((1, num_dates, num_paths), fixed_seed=fixed_seed)

        # Drift correction to keep jump to be risk neutral
        rj = self.lamb * (np.exp(self.mu + 0.5 * self.delta ** 2) - 1)

        short_rate = self.discount_curve.short_rate

        # simulate the paths
        for t in range(1, len(self.time_grid)):
            if self.correlated is False:
                random_num = sn1[t]
            else:
                # pick the correct random number when with correlation in portfolio context
                random_num = np.dot(self.cholesky_matrix, sn1[:, t, :])
                random_num = random_num[self.rn_set]

            # time difference as year fraction
            dt = (self.time_grid[t] - self.time_grid[t-1]).days / day_count

            # Poisson Distributed random numbers for jump component
            poi = np.random.poisson(self.lamb * dt, num_paths)

            # Apply Euler Discretization for Merton Jump Diffusion model
            paths[t] = paths[t-1] * (np.exp((short_rate - rj - 0.5 * self.volatility ** 2) * dt
                                    + self.volatility * np.sqrt(dt) * random_num)
                                    + (np.exp(self.mu + self.delta * sn2[t]) - 1) * poi)

        self.instrument_values = paths
