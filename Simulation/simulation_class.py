#
# QuantLibrary Simulation
# simulation_class.py
#
import numpy as np
import pandas as pd

class simulation_class(object):
    """
    A generic simulation class that provides base methods for simulation

    Atrributes:
    ===========
    name: string
        name of the simulation object
    mkt_env: instance of class market_environment
        mkt env data for simulation
    correlated: Boolean
        set if the simulation is correlated with other model objects

    Methods:
    ========
    generate_time_grid:
        returns time grid of relevant dates for simulation. Same for every simulation class
    get_instrument_values:
        return array of simulated instrument values. E.g. stock prices, commodities prices, volatilities
    """

    def __init__(self, name, mkt_env, correlated):
        # parsing a market_environment object
        # sanity check is skipped here for simplicity.
        # requiring extra carefulness when passing a market_environment object to any simulation class.
        try:
            self.name = name
            self.pricing_date = mkt_env.pricing_date
            self.initial_value = mkt_env.get_constant('initial_value')
            self.volatility = mkt_env.get_constant('volatility')
            self.final_date = mkt_env.get_constant('final_date')
            self.currency = mkt_env.get_constant('currency')
            self.frequency = mkt_env.get_constant('frequency')
            self.paths = mkt_env.get_constant('paths')
            self.discount_curve = mkt_env.get_curve('discount_curve')
            self.instrument_values = None
            self.correlated = correlated
            try:
                # if there is time_grid in mkt_env, set it
                # used for portfolio valuation
                self.time_grid = mkt_env.get_list('time_grid')
            except:
                self.time_grid = None

            try:
                # if there is special dates, set it
                self.special_dates = mkt_env.get_list('special_dates')
            except:
                self.special_dates = []

            if correlated is True:
                # decide if the risk factors are correlated
                # only required in portfolio evaluation
                self.cholesky_matrix = mkt_env.get_list('cholesky_matrix')
                self.rn_set = mkt_env.get_list('rn_set')[self.name]
                self.random_numbers = mkt_env.get_list('random_numbers')
        except:
            print "Error in parsing market environment!"

    def generate_time_grid(self):
        start = self.pricing_date
        end = self.final_date
        # pands date_range function
        # freq: B-Business day, W-Week, M-Month
        time_grid = pd.date_range(start=start, end=end, freq=self.frequency).to_pydatetime()
        time_grid = list(time_grid)

        # add  start, end and special_dates into time_grid if exist
        if start not in time_grid:
            time_grid.insert(0, start)
        if end not in time_grid:
            time_grid.append(end)
        if len(self.special_dates) > 0:
            time_grid.extend(self.special_dates)
            # remove duplicate dates
            time_grid = list(set(time_grid))
            # sort time_grid
            time_grid.sort()

        # parse time_grid into numpy.ndarray
        self.time_grid = np.array(time_grid)

    def get_instrument_values(self, fixed_seed=True):
        if self.instrument_values is None:
            # only generate simulation if there is no instrument values
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            # Additionly, re-generate simulation is fixed_seed is False
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)

        return self.instrument_values

    # method to be implemented in child class
    def generate_path(self):
        raise NotImplementedError("Need Implementation!")