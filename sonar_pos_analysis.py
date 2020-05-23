import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import plot_line, fit_func

SHOW_CAMERA_HEIGHT = False
WATER_INIT_HEIGHT = 0.126  # [m]

# DATA_PATH = '/home/avni1alon/alon/Lab/yalab/data/'
# DATA_PATH = 'data\\'
# DEFAULT_FILE_PATH = DATA_PATH + 'water_experiment_1_bach_2.csv'  # alon
DEFAULT_FILE_PATH = '..\\Results\\20.5.2020\\ex1.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW):
    experiment_data = pd.read_csv(file_path, header=header_row - 1,
                                  usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
        .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})
    return experiment_data


def smoothen_height_data(exp_data, rolling_window_size=30):
    exp_data['pos_error'] = exp_data.pos.rolling(window=rolling_window_size, center=True).std()
    exp_data['smoothened_pos'] = exp_data.pos.rolling(window=rolling_window_size, center=True).mean()


def plot_basic_height_data(exp_data, axes, plot_raw=True, plot_smoothened=True, save_plot=False, img_path=None):
    if plot_raw:
        exp_data.plot(x='time', y='pos', label='Raw position data', ax=axes, linestyle='None', marker='.')

    if plot_smoothened:
        assert 'smoothened_pos' in exp_data.columns, 'Error: data has not been smoothened!'

        exp_data.plot(x='time', y='smoothened_pos', label='Smoothened position data', ax=axes, grid=True,
                      linestyle='None', marker='x')

    plot_title = 'Height over time'
    plt.title(plot_title)
    plt.ylabel('Distance from sonar[m]')
    plt.xlabel('Time[s]')
    plt.legend()
    if save_plot:
        plt.savefig(f'{img_path}{plot_title}.png')


def get_real_water_height(exp_data, initial_height=WATER_INIT_HEIGHT):
    exp_data['water_height'] = initial_height + exp_data.pos.iloc[:200].mean() - exp_data.pos


def plot_water_height_data(exp_data, axes, fit_func_to_data=False, start_fit_time=3000, show_camera_height=False,
                           plot_residuals=False, residuales_axes=None, save_plots=False, img_path=None):
    exp_data.plot(x='time', y='water_height', label='Experimental data', grid=True, ax=axes, marker='.',
                  linestyle='None', alpha=0.7)

    if fit_func_to_data:
        # linear fit for position over time from a certain point
        linear_fit_data = exp_data[exp_data.time > start_fit_time]

        linear_func = lambda t, a, b: a * t + b
        [slope, intercept], errors = fit_func(linear_func, linear_fit_data.time, linear_fit_data.water_height)
        print(slope, intercept, errors)

        end_time = linear_fit_data.time.max()

        # plot linear fit
        fit_label = f'Linear fit\n({slope:.2e}$\pm${errors[0]:.2e})t+{intercept:.2e}$\pm${errors[1]:.2e}'
        plot_line(slope, intercept, x_range=[start_fit_time, end_time], axes=axes, plot_axes=False, label=fit_label,
                  c='k', zorder=12)

    # add camera dots
    if show_camera_height:
        # TODO: get this data as an input to the function
        camera_water_height = [0.125, 0.125, 0.125, 0.1225, 0.12, 0.115, 0.11, 0.10625, 0.1025, 0.1, 0.09, 0.0875,
                               0.085, 0.08375, 0.0825]
        camera_time = [0, 1800, 3600, 5400, 7200, 9000, 10800, 12600, 14400, 16200, 18000, 19800, 21600, 23400,
                       25200]

        plt.scatter(camera_time, camera_water_height, label='Camera Data', color='m', marker='x', zorder=5)

    axes.set_title('Water height over time')
    axes.set_ylabel('Height of Water[m]')
    axes.set_xlabel('Time[s]')
    axes.legend()
    if save_plots:
        axes.savefig(f'{img_path}Linear fit to part of height over time data.png')

    if plot_residuals:
        sns.residplot(linear_fit_data.time, linear_fit_data.water_height, ax=residuales_axes)

        residuales_axes.set_title('Residuals plot for linear fit')
        residuales_axes.set_ylabel('$\Delta$h error[m]')
        residuales_axes.set_xlabel('Time[s]')
        if save_plots:
            residuales_axes.savefig(f'{img_path}Residuals plot.png')
