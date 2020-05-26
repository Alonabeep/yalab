import matplotlib.pyplot as plt
import seaborn as sns

from utils import plot_line, fit_func

SHOW_CAMERA_HEIGHT = False
WATER_INIT_HEIGHT = 0.126  # [m]

DATA_PATH = '/home/avni1alon/alon/Lab/yalab/data/' # alon
DEFAULT_FILE_PATH = DATA_PATH + 'water_experiment_1_bach_1.csv'  # alon
# DEFAULT_FILE_PATH = '..\\Results\\20.5.2020\\ex1.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def smoothen_height_data(exp_data, rolling_window_size=30):
    exp_data['pos_error'] = exp_data.pos.rolling(window=rolling_window_size, center=True).std()
    exp_data['smoothened_pos'] = exp_data.pos.rolling(window=rolling_window_size, center=True).mean()


def plot_basic_height_data(exp_data, axes, plot_raw=True, plot_smoothened=True, save_plot=False, img_path=None,
                           temp_label=False):
    if plot_raw:
        exp_data.plot(x='time', y='pos', label='Raw position data', ax=axes, linestyle='None', marker='.')

    if plot_smoothened:
        assert 'smoothened_pos' in exp_data.columns, 'Error: data has not been smoothened!'

        if temp_label:
            measurement_temp = round(exp_data.temp.quantile(0.6))
            smoothened_label = f'{measurement_temp:.0f}$\degree$C measurement data'
        else:
            smoothened_label = 'Smoothened position data'

        exp_data.plot(x='time', y='smoothened_pos', label=smoothened_label, ax=axes, grid=True,
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
                           plot_residuals=False, residuales_axes=None, save_plots=False, img_path=None, fit_line=None,
                           label_fit=False, temp_label=False, **kwargs):
    if temp_label:
        measurement_stable_temp = round(exp_data.temp.quantile(0.6))
        data_label = f'{measurement_stable_temp:.0f}$\degree$C measurement data'
    else:
        data_label = 'Experimental data'
    exp_data.plot(x='time', y='water_height', label=data_label, grid=True, ax=axes, linestyle='None', alpha=0.4,
                  **kwargs)

    if fit_func_to_data:
        # linear fit for position over time from a certain point
        linear_fit_data = exp_data[exp_data.time > start_fit_time]

        linear_func = lambda t, a, b: a * t + b
        [slope, intercept], errors = fit_func(linear_func, linear_fit_data.time, linear_fit_data.water_height)
        print(f'slope - {slope}, {intercept} - intercept, errors - {errors}')

        end_time = linear_fit_data.time.max()

        # plot linear fit
        if label_fit:
            fit_label = f'Linear fit\n({slope:.2e}$\pm${errors[0]:.2e})t+{intercept:.2e}$\pm${errors[1]:.2e}'
        else:
            fit_label = None
        plot_line(slope, intercept, x_range=[start_fit_time, end_time], axes=axes, plot_axes=False, label=fit_label,
                  c='k', zorder=12, linestyle='-' if fit_line is None else fit_line)

    # add camera dots
    if show_camera_height:
        axes.scatter(camera_time, camera_water_height, label='Camera Data', color='m', marker='x', zorder=5)

    axes.set_title('Water height over time')
    axes.set_ylabel('Height of Water[m]')
    axes.set_xlabel('Time[s]')
    axes.legend()
    if save_plots:
        axes.savefig(f'{img_path}Linear fit to part of height over time data.png')
        #plot = exp_data.plot()
        #fig1 = plot.get_figure()
        #fig1.savefig(DATA_PATH + f'{img_path}Linear fit to part of height over time data.png')

    if plot_residuals:
        sns.residplot(linear_fit_data.time, linear_fit_data.water_height, ax=residuales_axes)

        residuales_axes.set_title('Residuals plot for linear fit')
        residuales_axes.set_ylabel('$\Delta$h error[m]')
        residuales_axes.set_xlabel('Time[s]')
        if save_plots:
            residuales_axes.savefig(f'{img_path}Residuals plot.png')
