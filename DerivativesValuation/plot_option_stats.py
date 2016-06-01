#
# Helper function to plot options stats
#  #

import matplotlib.pyplot as plt

def plot_option_stats (strike_list, price_list, delta_list, vega_list):
    '''
    Helper function to plot option prices, deltas and vegas
    for a set of underlying initial values

    :param strike_list: array or list
            set of initial values of the underlying
    :param price_list: array or list
            present values of option
    :param delta_list: array or list
            option deltas
    :param vega_list: array or list
            option vegas
    '''

    plt.figure(figsize=(9,7))
    sub1 = plot.subplot(311)
    plt.plot(strike_list, price_list, 'ro', label='present value')
    plt.plot(strike_list, price_list, 'b')
    plt.grid(True)
    plt.legend(loc=0)
    plt.setp(sub1.get_xticklabels(), visible=False)