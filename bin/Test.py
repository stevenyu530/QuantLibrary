from DeriativesAnalysisLibrary import *
from constant_short_rate import *


dates = [dt.datetime(2015,1,1), dt.datetime(2015,7,1), dt.datetime(2016,1,1)]
print get_year_deltas(dates)

csr = constant_short_rate('csr', 0.05)
print csr.get_discount_factors(dates)
