import matplotlib.pyplot as plt
import pandas as pd

from sonar_pos_analysis import plot_water_height_data, get_real_water_height, plot_basic_height_data
from temp_pos_analysis import plot_temp_over_time_data

DATA_PATH = '/home/avni1alon/alon/Lab/yalab/data/' # alon
DEFAULT_FILE_PATH = DATA_PATH + 'water_experiment_3_bach_1.csv'  # alon
# DEFAULT_FILE_PATH = '..\\Results\\20.5.2020\\ex1.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW):
    experiment_data = pd.read_csv(file_path, header=header_row - 1,
                                  usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
        .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

    return experiment_data

def load_camera_data():
    camera_water_height1 = [0.125, 0.125, 0.125, 0.1225, 0.12, 0.115, 0.11, 0.10625, 0.1025, 0.1, 0.09, 0.0875, 0.085, 0.08375, 0.0825]
    camera_time1 = list(range(0, 11*1800, 1800)) + [19755, 20355, 20955, 21555]
    camera_water_height2 = [0.12375,0.11875,0.12375,0.1175,0.1125,0.1075,0.10375,0.1,0.09125,0.0875,0.0825,0.075,0.07]
    camera_time2 = [2230, 3730, 5230, 6730, 8230, 9730, 11230, 12730, 14230, 15730, 17230, 18730, 20230]
    camera_water_height3 = [0.10875, 0.1, 0.09, 0.08, 0.07, 0.06]
    camera_time3 = list(range(0, 6*1500, 1500))
    return camera_water_height1, camera_time1, camera_water_height2, camera_time2, camera_water_height3, camera_time3


if __name__ == '__main__':
    exp_data = read_experiment_data()

    camera_water_height1, camera_time1, camera_water_height2, camera_time2, camera_water_height3, camera_time3 = load_camera_data()

    
    temp_amplitude = exp_data.temp.max() - exp_data.temp.min()
    # start the linear fit only when the temperature reaches its 90th percentile
    temp_start_fit_threshold = exp_data.temp.min() + 0.9 * temp_amplitude
    start_fit_time = exp_data.time[exp_data.temp > temp_start_fit_threshold].iat[0]

    fig, axs = plt.subplots(2, sharex=True)

    get_real_water_height(exp_data)
    plot_water_height_data(exp_data, axes=axs[0], fit_func_to_data=True, start_fit_time=start_fit_time, show_camera_height=True, 
                           camera_water_height=camera_water_height3, camera_time=camera_time3, save_plots=False)
    
    plot_temp_over_time_data(exp_data, axs[1])

    '''
    # make them have the same x axis
    plt.subplots_adjust(hspace=0)
    for ax in axs:
        ax.set_title('')
    '''

    plt.show()
