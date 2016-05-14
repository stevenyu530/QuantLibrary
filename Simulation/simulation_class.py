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
    get_instrument_value:
        return array of simulated instrument values. E.g. stock prices, commodities prices, volatilities
    """

    def __init__(self, name, mkt_env, correlated):
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


    