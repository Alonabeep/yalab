import matplotlib.pyplot as plt

from utils import fit_and_plot_line

if __name__ == '__main__':
    rate_of_evaporation = [6.85E-05,
                           3.29E-05,
                           0.000047,
                           1.78E-05,
                           0.00007,
                           0.0000085]
    roe_max_error = [5.15366E-06,
                     4.73856E-06,
                     3.88155E-06,
                     1.78355E-06,
                     6.86275E-06,
                     5.85015E-07]
    power = [1667.155,
             780.75,
             1194.175,
             420.2315,
             1646.4825,
             246.74]
    power_max_error = [24,
                       13.41,
                       16.61,
                       9.816,
                       19.54,
                       9.22]
    avg_boiling_temp = [97.57,
                        97.39,
                        97.44,
                        97.46,
                        97.42,
                        96.98]

    fig_name = 'RoE vs Power'
    plt.figure(fig_name)
    plt.errorbar(power, rate_of_evaporation, xerr=power_max_error, yerr=roe_max_error, marker='.', linestyle='None',
                 ecolor='r', zorder=99, ms=10)
    [slope, intercept], errors = fit_and_plot_line(power, rate_of_evaporation, fig=fig_name,
                                                   x_range=[-10, max(power) * 1.05])

    plt.legend([f'Linear fit\n({slope:.1e}$\pm${errors[0]:.1e})p{intercept:.1e}$\pm${errors[1]:.1e}',
                'Experimental Data'])
    plt.title('Rate of evaporation vs. Power')
    plt.ylabel('Rate of evaporation [m/s]')
    plt.xlabel('Power [W]')
    plt.grid(zorder=-12)
    plt.tight_layout()

    fig_name = 'Avg temp vs Power'
    plt.figure(fig_name)
    plt.errorbar(power, avg_boiling_temp, xerr=power_max_error, marker='.', linestyle='None', ecolor='r', zorder=99,
                 ms=10)

    for tick in plt.gca().yaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')

    plt.xlabel('Power [W]')
    plt.title('Average boiling temperature vs. Power')
    plt.ylabel('Average boiling temperature [$\degree$C]', fontweight='bold')
    plt.grid(zorder=-12)

    plt.tight_layout()
    plt.show()
