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
    experiment_data = {'rate_of_evaporation': [2.20e-7, 1.35e-6, 2.24e-6, 4.13e-6, 8.63e-6],
                       'water_temp': [40, 70, 79, 91, 97],
                       'roe_error': [3.59e-9, 1.16e-8, 2.03e-8, 4.56e-8, 2.79e-7],
                       'temp_error': [1.5] * 4 + [1]}
    home_experiment_data = {'rate_of_evaporation': [1.88e-5, 6.17e-6, 1.63e-5],
                            'water_temp': [100.3, 101.4, 102],
                            'roe_error': [1.36e-6, 6.2e-8, 2.28e-7],
                            'temp_error': [2] * 3}

    plt.errorbar(experiment_data['water_temp'], experiment_data['rate_of_evaporation'],
                 yerr=experiment_data['roe_error'], xerr=experiment_data['temp_error'], ecolor='r', capsize=2,
                 marker='o', linestyle='None', zorder=999, label='Lab Experiments Data')
    plt.errorbar(home_experiment_data['water_temp'], home_experiment_data['rate_of_evaporation'],
                 yerr=home_experiment_data['roe_error'], xerr=home_experiment_data['temp_error'],
                 ecolor='r', capsize=2, marker='d', c='m', linestyle='None', zorder=998,
                 label='Home Experiments Data')

    func_to_fit = lambda temp, power, amplitude, offset: amplitude * temp ** (power) + offset

    plt.semilogy()
    plt.grid(zorder=-1)
    plt.ylabel('Rate of evaporation[m/s]')
    plt.xlabel('Measurement temperature[$\degree$C]')
    plt.title('Rate of evaporation vs measurement temperature')
    plt.legend()
    plt.show()
