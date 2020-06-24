import matplotlib.pyplot as plt

from utils import plot_line, fit_func


def fit_line(experiment_data):
    linear_func = lambda t, a, b: a * t + b
    [slope, intercept], errors = fit_func(linear_func, experiment_data['water_temp'],
                                          experiment_data['rate_of_evaporation'])
    print(f'slope - {slope}, {intercept} - intercept, errors - {errors}')
    start_fit_temp = experiment_data['water_temp'][0]
    end_temp = experiment_data['water_temp'][3]
    fit_label = f'Linear fit\n({slope:.2e}$\pm${errors[0]:.2e})t+{intercept:.2e}$\pm${errors[1]:.2e}'
    plot_line(slope, intercept, x_range=[start_fit_temp, end_temp], plot_axes=False, label=fit_label,
              c='k', zorder=12)


if __name__ == '__main__':
    experiment_data = {'rate_of_evaporation': [4.17e-7, 1.90e-6, 2.71e-6, 5.03e-6, 8.63e-6, 1.89e-8, 3.46e-6],
                       'water_temp': [39.2, 71.5, 79.5, 91.3, 97.2, 23, 85.6],
                       'roe_error': [5.6e-8, 2.2e-8, 2.00e-8, 5.33e-8, 1.04e-6, 1.72e-9, 2.55e-7],
                       'temp_error': [0.4, 1.5, 1.5, 1.2, 0.7, 1.5, 0.8]}
    home_experiment_data = {'rate_of_evaporation': [1.88e-5, 6.17e-6, 1.63e-5],
                            'water_temp': [100.3, 101.4, 102],
                            'roe_error': [1.36e-6, 6.2e-8, 2.28e-7],
                            'temp_error': [2] * 3}
    kettle_experiment_data = {
        'rate_of_evaporation': [6.84783E-05, 3.28571E-05, 0.000047, 1.77632E-05, 0.00007, 0.0000085],
        'water_temp': [97.57, 97.39, 97.44, 97.46, 97.42, 96.98],
        'roe_error': [5.15366E-06, 4.73856E-06, 3.88155E-06, 1.78355E-06, 6.86275E-06,
                      5.85015E-07]}

    plt.errorbar(experiment_data['water_temp'], experiment_data['rate_of_evaporation'],
                 yerr=experiment_data['roe_error'], xerr=experiment_data['temp_error'], ecolor='r', capsize=2,
                 marker='o', linestyle='None', zorder=999, label='Heat Plate Experiments Data', c='b')
    # plt.errorbar(home_experiment_data['water_temp'], home_experiment_data['rate_of_evaporation'],
    #              yerr=home_experiment_data['roe_error'], xerr=home_experiment_data['temp_error'],
    #              ecolor='r', capsize=2, marker='d', c='m', linestyle='None', zorder=998,
    #              label='Home Experiments Data')
    plt.errorbar(kettle_experiment_data['water_temp'], kettle_experiment_data['rate_of_evaporation'],
                 yerr=kettle_experiment_data['roe_error'], ecolor='r', capsize=2, marker='X', c='darkgreen',
                 linestyle='None', zorder=998.5, label='Kettle Experiments Data', ms=7)

    plt.annotate('Heat plate data',
                 (experiment_data['water_temp'][1] - 5, experiment_data['rate_of_evaporation'][1] + 1e-6), ha='center',
                 c='b')

    plt.annotate('Kettle data',
                 (kettle_experiment_data['water_temp'][1] - 7, kettle_experiment_data['rate_of_evaporation'][1] + 1e-6),
                 ha='center', c='darkgreen')

    plt.semilogy()
    plt.grid(zorder=-1)
    plt.ylabel('Rate of evaporation[m/s]')
    plt.xlabel('Measurement temperature[$\degree$C]')
    plt.title('Rate of evaporation vs measurement temperature')
    # plt.legend()
    plt.tight_layout()

    plt.show()
