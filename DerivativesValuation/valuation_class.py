class valuation_class(object):
    '''
    generic class for single-factor valuation

    Atrributes:
    ===========
    name: string
        name of the object
    underlying:
        instance of simulation class
    mkt_env: instance of market_environment

    payoff_function: string
        derivatives payoff function to be used as lambda expression.
        e.g.: 'np.maximum(maturity_value-100, 0)'

    Methods:
    ========
    update:
        update the the selected valuation paramenters
    delta:
        return the delta of the derivative
    vega:
        return the Vega of the derivative
    '''

    def __init__(self, name, underlying, mkt_env, payoff_function = ''):
        try:
            self.name = name
            self.pricing_date = mkt_env.pricing_date
            try:
                self.strike = mkt_env.get_constant('strike')    # strike is optional
            except:
                pass
            self.maturity = mkt_env.get_constant('maturity')
            self.currency = mkt_env.get_constant('currency')

            # from simulation object, parse simulation parameters and discount curve
            self.frequency = underlying.frequency
            self.paths = underlying.paths
            self.discount_curve = underlying.discount_curve
            self.underlying = underlying
            self.payoff_func = payoff_function

            self.underlying.special_dates.extend([self.pricing_date, self.maturity])
        except:
            print "Error parsing market environment"

    def update(self, initial_value=None, volatility=None, strike=None, maturity=None):
        if initial_value is not None:
            self.underlying.update(initial_value=initial_value)
        if volatility is not None:
            self.underlying.update(volatility=volatility)
        if strike is not None:
            self.strike=strike
        if maturity is not None:
            self.maturity = maturity
            # add new maturity date if not in time_grid
            if not maturity in self.underlying.time_grid:
                self.underlying.special_dates.append(maturity)
                self.underlying.instrument_values = None

    def delta(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value / 50.
        # forward-difference approximation, calculate the left value for numerical Delta
        value_left = self.present_value(fixed_seed=True)
        # numerical underling value for right value
        initial_delta = self.underlying.initial_value + interval
        self.underlying.update(initial_value=initial_delta)
        # calculate right value for numberical delta
        value_right = self.present_value(fixed_seed=True)
        # reset the initial_value of the simulation object
        self.underlying.update(initial_value=initial_delta-interval)
        delta = (value_right - value_left) / interval

        # correct for potential numerical errors
        if delta < -1.0:
            return -1.0
        elif delta > 1.0:
            return 1.0
        else:
            return round(delta, accuracy)

    def vega(self, interval=0.01, accuracy=4):
        if interval < self.underlying.volatility / 50.:
            interval = self.underlying.volatility / 50.
        # forward-difference approximation, calculate the left value for numerical Vega
        value_left = self.present_value(fixed_seed=True)
        # numerical vol value for the right value
        vol_delta = self.underlying.volatility + interval
        # update the simulation object
        self.underlying.update(volatility=vol_delta)
        # right value for numerical Vega
        value_right = self.present_value(fixed_seed=True)
        # reset vol value of simulation object
        self.underlying.update(volatility=vol_delta-interval)
        vega = (value_right - value_left) / interval
        return round(vega, accuracy)