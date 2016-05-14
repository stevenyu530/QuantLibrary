from Simulation import *

sn_rn = sn_random_numbers((2,2,2), antithetic=False, moment_matching=False, fixed_seed=True )
print sn_rn


sn_rn_mm = sn_random_numbers((2,3,2), antithetic=False, moment_matching=True, fixed_seed=True)
print "\n>>>"
print sn_rn_mm
print sn_rn_mm.mean()
print sn_rn_mm.std()


