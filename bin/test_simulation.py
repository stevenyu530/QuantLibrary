from ValuationFramework import *
from Simulation import *
import matplotlib.pyplot as plt


print ">>> Testing sn_random_numbers.py\n"
sn_rn = sn_random_numbers((2,2,2), antithetic=False, moment_matching=False, fixed_seed=True )
print sn_rn

sn_rn_mm = sn_random_numbers((2,3,2), antithetic=False, moment_matching=True, fixed_seed=True)
print "\n"
print sn_rn_mm
print sn_rn_mm.mean()
print sn_rn_mm.std()


print "\n\n================"
print ">>> Testing geometric_brownian_motion.py\n"
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


print "\n\n"
paths_1 = gbm.get_instrument_values()
print paths_1

print "\n plot simulated paths"
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()

plt.figure(figsize=(12,6))
p1 = plt.plot(gbm.time_grid, paths_1[:,:10], 'b')
p2 = plt.plot(gbm.time_grid, paths_2[:,:10], 'r-.')
plt.grid(True)
plt.title("GBM Simulation")
l1 = plt.legend([p1[0], p2[0]], ['low vol', 'high vol'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()


print "\n\n================"
print ">>> Testing merton_jump_diffusion.py\n"
mkt_env_mjd = market_environment('mkt_env_mjd', dt.datetime(2016,1,1))

# Add Merton Jump Diffusion parameters
mkt_env_mjd.add_constant('lambda', 0.3)
mkt_env_mjd.add_constant('mu', -0.75)
mkt_env_mjd.add_constant('delta', 0.1)
mkt_env_mjd.add_environment(mkt_env_gbm)

mjd = merton_jump_diffusion('mjd', mkt_env_mjd)

paths_3 = mjd.get_instrument_values()
print "\n low lambda\n"
print paths_3

mjd.update(lamb=0.9)
paths_4 = mjd.get_instrument_values()
print "\n high lambda\n"
print paths_4

plt.figure(figsize=(12,6))
p1 = plt.plot(gbm.time_grid, paths_3[:, :10], 'b')
p2 = plt.plot(gbm.time_grid, paths_4[:, :10], 'r-.')
plt.grid(True)
plt.title("Merton Jumpy Simulation")
l1 = plt.legend([p1[0], p2[0]], ['low intensity(lambda)', 'high intensity(lambda)'], loc=3)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()


print "\n\n================"
print ">>> Testing square_root_diffusion.py\n"
# set up market environment parametersR
mkt_env_srd = market_environment('mkt_env_srd', dt.datetime(2016, 1, 1))
mkt_env_srd.add_constant('initial_value', 0.25)
mkt_env_srd.add_constant('volatility', 0.05)
mkt_env_srd.add_constant('final_date', dt.datetime(2016,12,31))
mkt_env_srd.add_constant('currency', 'EUR')
mkt_env_srd.add_constant('frequency', 'W')
mkt_env_srd.add_constant('paths', 10000)
mkt_env_srd.add_constant('kappa', 4.0)
mkt_env_srd.add_constant('theta', 0.2)
mkt_env_srd.add_curve('discount_curve', constant_short_rate('r', 0.0))

# initialize simulation class
srd = square_root_diffusion('srd', mkt_env_srd)
srd_paths = srd.get_instrument_values()

plt.figure(figsize=(12, 6))
plt.plot(srd.time_grid, srd_paths[:, :10])
plt.axhline(mkt_env_srd.get_constant('theta'), color='r', ls='--', lw=2.0)
plt.grid(True)
plt.title("Square-Root Diffusion Simulation")
plt.xticks(rotation=30)
plt.show()


