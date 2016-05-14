from ValuationFramework import *
from Simulation import *
import matplotlib.pyplot as plt


sn_rn = sn_random_numbers((2,2,2), antithetic=False, moment_matching=False, fixed_seed=True )
print sn_rn


sn_rn_mm = sn_random_numbers((2,3,2), antithetic=False, moment_matching=True, fixed_seed=True)
print "\n>>>"
print sn_rn_mm
print sn_rn_mm.mean()
print sn_rn_mm.std()


print "\n\n================"
mkt_env_gbm = market_environment('mkt_env_gbm', dt.datetime(2016,1,1))
mkt_env_gbm.add_constant('initial_value', 36.)
mkt_env_gbm.add_constant('volatility', 0.2)
mkt_env_gbm.add_constant('final_date', dt.datetime(2016,12,31))
mkt_env_gbm.add_constant('currency', 'EUR')
mkt_env_gbm.add_constant('frequency', 'M')
mkt_env_gbm.add_constant('paths', 10000)

r = constant_short_rate('r', 0.05)
mkt_env_gbm.add_curve('discount_curve', r)

gbm = geometric_brownian_motion('gbm', mkt_env_gbm)
gbm.generate_time_grid()
print gbm.time_grid


print "\n\n================"
paths_1 = gbm.get_instrument_values()
print paths_1


print "\n\n================"
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()

plt.figure(figsize=(15,8))
p1 = plt.plot(gbm.time_grid, paths_1[:,:10], 'b')
p2 = plt.plot(gbm.time_grid, paths_2[:,:10], 'r-.')
plt.grid(True)
l1 = plt.legend([p1[0], p2[0]], ['low vol', 'high vol'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()