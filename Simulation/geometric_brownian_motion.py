#
# QuantLibrary Simulation
# geometric_brownian_motion.py
#

import numpy as np
from sn_random_numbers import sn_random_numbers
from simulation_class import simulation_class

class geometric_brownian_motion(simulation_class):
    """
    Class to generate GBM simulated paths based on BS GBM model
    Euler scheme is applied in discretision

    Attributes
    ==========
    name: string
        name of the object
    mkt_evn: instance of market_environment class
        mkt data for simulation
    correlated: Boolean
        Decide if correlated with other model simulation object

    Methods
    =======
    update:
        update param values
    generate_paths:
        override the method in simulation_class
        returns Monte Carlo simulated paths given the the mkt environment
    """

    def __init__(self, name, mkt_env, correlated=False):
        super(geometric_brownian_motion, self).__init__(name, mkt_env, correlated)


    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None


    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()

        # initialization for path simulation, and initialize the first date
        num_dates = len(self.time_grid)
        num_paths = self.paths
        paths = np.zeros((num_dates, num_paths))
        paths[0] = self.initial_value

        if not self.correlated:
            # if not correlated, generate random numbers
            random_nums = sn_random_numbers((1, num_dates, num_paths), fixed_seed=fixed_seed)
        else:
            # if correlated, use provided random numbers from mkt env
            random_nums = self.random_numbers

        # get the short rate for GBM drift
        short_rate = self.discount_curve.short_rate

        # generate the paths
        for t in range(1,len(self.time_grid)):
            # choose the correct time step
            # depending on if correalted
            if not self.correlated:
                rand = random_nums[t]
            else:
                rand = np.dot(self.cholesky_matrix, random_nums[:,t,:])
                rand = rand(self.rn_set)

            # calculate dt: difference between two simulated dates in year's fraction
            dt = (self.time_grid[t] - self.time_grid[t-1]).days / day_count
            # generate the simulated values at the current time grid
            paths[t] = paths[t-1] * np.exp((short_rate - 0.5*self.volatility**2)*dt
                                           + self.volatility*np.sqrt(dt) * rand)

        self.instrument_values = paths

