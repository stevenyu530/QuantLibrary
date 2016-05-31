import numpy as np
from valuation_class import valuation_class

class valuation_european (valuation_class):
    """
    Class to value vanilla European Options with arbitrary payoff functions
    using single-factor Monte Carlo Simulation.

    Methods
    ========
    generate_payoff:
        returns payoffs givent the simulated paths and the payoff function
    present_value:
        returns present value, with Monte Carlo Estimation
    """

    def generate_payoff(self, fixed_seed=False):
        '''
        :param fixed_seed: Boolean
            decide if to use fixed seed for valuation
        '''

        try:
            # strike defined?
            strike = self.strike
        except:
            pass
        paths = self.underlying.get_instrument_values(fixed_seed=fixed_seed)
        time_grid = self.underlying.time_grid
        try:
            time_index = np.where(time_grid == self.maturity)[0]
            time_index = int(time_index)
        except:
            print "Maturity date not in time grid of underlying"
        maturity_value = paths[time_index]

        # average value of the whole path
        mean_val = np.mean(paths[:time_index], axis=1)
        # maximum value of the whole path
        max_val = np.amax(paths[:time_index], axis=1)[-1]
        # minimum value of the whole path
        min_val = np.amin(paths[:time_index], axis=1)[-1]

        try:
            payoff = eval(self.payoff_func)
            return payoff
        except:
            print "Error evaluating payoff function."

    def present_value(self, accuracy=6, fixed_seed=False, full=False):
        '''
        :param accuracy: int
                number of decimals in returned value
        :param fixed_seed: Boolean
                decide if to use fixed sedd for valuation
        :param full: Boolean
                decide if to also return a 1D array of present values
        '''
        cash_flow = self.generate_payoff(fixed_seed=fixed_seed)
        discount_factor = self.discount_curve.get_discount_factors((self.pricing_date, self.maturity))[0,1]
        value = discount_factor * np.sum(cash_flow) / len(cash_flow)

        if full:
            return round(value, accuracy), discount_factor * cash_flow
        else:
            return round(value, accuracy)