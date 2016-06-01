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
    sub1 = plt.subplot(311)
    plt.plot(strike_list, price_list, 'ro', label='present value')
    plt.plot(strike_list, price_list, 'b')
    plt.grid(True)
    plt.legend(loc=0)
    plt.setp(sub1.get_xticklabels(), visible=False)

    sub2 = plt.subplot(312)
    plt.plot(strike_list, delta_list, 'go', label='Delta')
    plt.plot(strike_list, delta_list, 'b')
    plt.grid(True)
    plt.legend(loc=0)
    plt.ylim(min(delta_list) - 0.1, max(delta_list)+0.1)
    plt.setp(sub2.get_xticklabels(), visible=False)

    sub3 = plt.subplot(313)
    plt.plot(strike_list, vega_list, 'yo', label='Vega')
    plt.plot(strike_list, vega_list, 'b')
    plt.xlabel('initial valufe of underlying')
    plt.grid(True)
    plt.legend(loc=0)

    plt.show()
