import matplotlib.pyplot as plt
import numpy as np

from main import read_experiment_data

if __name__ == '__main__':
    experiments_data_paths = ['..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv',
                              '..\\Results\\18.5.2020\\exp1 - last run only.csv',
                              '..\\Results\\20.5.2020\\ex1.csv']

    bubbles_per_experiment = [[0,
                               5,
                               4,
                               3,
                               3,
                               3,
                               3,
                               2,
                               2,
                               2],
                              [2,
                               2,
                               2,
                               1,
                               1,
                               1,
                               0,
                               0,
                               0,
                               0,
                               0,
                               0,
                               0],
                              [0,
                               0.05,
                               0.1,
                               0.15,
                               0.2,
                               0.25,
                               0.3,
                               0.35,
                               0.4,
                               0.45,
                               0.5,
                               0.55,
                               0.6,
                               0.65,
                               0.7,
                               0.75,
                               0.8,
                               0.85,
                               0.9,
                               0.95,
                               1,
                               1.05,
                               1.1,
                               1.15,
                               1.2,
                               1.25,
                               3,
                               3,
                               2,
                               2,
                               2,
                               2,
                               1.9,
                               1.8,
                               1.7,
                               1.6,
                               1.5,
                               1.4,
                               1.3,
                               1.2,
                               1.1,
                               1,
                               0.9,
                               0.8,
                               0.7,
                               0.6,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5,
                               0.5]]
    camera_time = [list(range(0, 11 * 1800, 1800))[:10],
                   [2230, 3730, 5230, 6730, 8230, 9730, 11230, 12730, 14230, 15730, 17230, 18730, 20230],
                   list(np.linspace(0, 13 * 60, 26)) +
                   list(np.linspace(1140, 1140 + 90 * 30, 91))]

    exp_num = 2

    exp_data = read_experiment_data(experiments_data_paths[exp_num])

    exp_data['delta_t'] = exp_data.time.diff(periods=25)
    exp_data['delta_temp'] = exp_data.temp.diff(periods=25)
    exp_data['temp_change_over_time'] = exp_data.apply(lambda data: data.delta_temp / data.delta_t, axis='columns')

    exp_data.plot(x='time', y='temp_change_over_time', grid=True, label='Calculated Derivative', zorder=22)

    plt.gca().set_ylabel('dT/dt[$\degree$C]')
    plt.legend()

    scale_const = 75
    secondary_axis = plt.gca().secondary_yaxis('right',
                                               functions=(lambda x: x * scale_const, lambda x: x / scale_const))
    plt.bar(camera_time[exp_num], np.array(bubbles_per_experiment[exp_num]) / scale_const, width=20, zorder=12,
            color='k', label='Amount of bubbles over time')
    secondary_axis.set_ylabel('Amount of bubbles')

    plt.xlabel('Time[s]')

    plt.title('Temperature rate of change and amount of bubbles over time')

    plt.legend()

    plt.tight_layout()
    plt.show()
