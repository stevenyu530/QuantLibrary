from Framework import *


dates = [dt.datetime(2015,1,1), dt.datetime(2015,7,1), dt.datetime(2016,1,1)]
csr = constant_short_rate('csr', 0.05)

mkt1 = market_environment('mkt1', dt.datetime(2015,1,1))
mkt1.add_list('symbols', ['APPL', 'MSFT', 'FB'])
print mkt1.get_list('symbols')

mkt2 = market_environment('mkt2', dt.datetime(2015,1,1))
mkt2.add_constant('volatility', 0.2)
mkt2.add_curve('short_rate', csr) # add instance of discounting class
print mkt2.get_curve('short_rate')

mkt1.add_environment(mkt2)
print mkt1.get_curve('short_rate')

print mkt1.constants
print mkt1.lists
print mkt1.curves
print mkt1.get_curve('short_rate').short_rate