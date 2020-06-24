import matplotlib.pyplot as plt
import numpy as np

from utils import fit_func, plot_func

if __name__ == '__main__':
    rate_of_volume_evaporation = np.array([1.19e-5,
                                           4.96e-5,
                                           2.28e-5])
    rove_max_error = np.array([8.82e-7,
                               2.32e-6,
                               1.84e-6])
    area = [5.80e-3,
            2.14e-2,
            1e-2]
    area_max_error = [1.68e-4,
                      4.63e-4,
                      1.77e-4]

    fig_name = 'RoE vs Area'
    plt.figure(fig_name)
    plt.errorbar(area, rate_of_volume_evaporation, xerr=area_max_error, yerr=rove_max_error, marker='.',
                 linestyle='None', ecolor='r', zorder=99, ms=10, c='m')
    coefficient, err = fit_func(lambda x, a: a * x, area, rate_of_volume_evaporation)
    plot_func(lambda x: coefficient * x, [0, max(area) * 1.1], c='k', linestyle='--')
    plt.annotate(f'y=({coefficient[0]:.2e}$\pm${err[0]:.2e})x', (1e-2, max(rate_of_volume_evaporation)),
                 ha='center', c='k', fontsize=13,
                 bbox=dict(facecolor='wheat', alpha=0.5, edgecolor='black', boxstyle='round,pad=1'))

    plt.title('Rate of volume evaporation vs. Area in contact with air', fontsize=16)
    plt.ylabel('Rate of volume evaporation [l/s]', fontsize=14)
    plt.xlabel('Area in contact with air [m$^2$]', fontsize=14)
    plt.grid(zorder=-12)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    plt.show()
