from DerivativesValuation import *
from Simulation import *
from ValuationFramework import *
import numpy as np


# Construct an underling option to be valued
mkt_gbm = market_environment('mkt_gbm', dt.datetime(2015,1,1))
mkt_gbm.add_constant('initial_value', 36.)
mkt_gbm.add_constant('volatility', 0.2)
mkt_gbm.add_constant('final_date', dt.datetime(2015,12,31))
mkt_gbm.add_constant('currency', 'EUR')
mkt_gbm.add_constant('frequency', 'M')
mkt_gbm.add_constant('paths', 10000)
rate = constant_short_rate('rate', 0.06)
mkt_gbm.add_curve('discount_curve', rate)

gbm = geometric_brownian_motion('gbm', mkt_gbm)

# construct mkt_env for the option
mkt_call = market_environment('mkt_call', mkt_gbm.pricing_date)
mkt_call.add_constant('strike', 40.)
mkt_call.add_constant('maturity', dt.datetime(2015,12,31))
mkt_call.add_constant('currency', 'EUR')

# payoff function for the simulated call option
payoff_func = 'np.maximum(maturity_value - strike, 0)'
eur_call = valuation_european('eur_call', underlying=gbm, mkt_env=mkt_call, payoff_function=payoff_func)

# test individual method result
print 'present value = %.4f' % eur_call.present_value()
print 'delta = %.4f' % eur_call.delta()
print 'vega = %.4f' % eur_call.vega()

# test the values for a range of underlyings
strike_list = np.arange(34., 46.1, 2.)
price_list = []
delta_list = []
vega_list = []
for strike in strike_list:
    eur_call.update(initial_value=strike)
    price_list.append(eur_call.present_value(fixed_seed=True))
    delta_list.append(eur_call.delta())
    vega_list.append(eur_call.vega())

print price_list
print delta_list
print vega_list