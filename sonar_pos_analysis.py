import matplotlib.pyplot as plt
import pandas as pd
import utils as ut
import numpy as np

file_path = '/home/avni1alon/alon/Lab/data/try.csv'

relevant_cols = 'A:D'
header_row = 1
plt.figure('sonar position')

experiment_data = pd.read_csv(file_path, header=header_row - 1,
                              usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

# normelize the position
experiment_data["pos"]=(experiment_data["pos"][0] - experiment_data["pos"])

# fit fot pos
start_fit_time = 250
end_fit_time = 2234
def test_func(t, a, b):
    return a * t + b
slope1, intercept1 = ut.fit_func(test_func, experiment_data["time"][start_fit_time:end_fit_time], experiment_data["pos"][start_fit_time:end_fit_time])
start_constant = experiment_data["pos"][start_fit_time-50:start_fit_time+50].mean()

# smoothen the position data and show the unsmoothed and smoothed data on the same graph
axes = plt.gca()
experiment_data.plot(x='time', y='pos', label='raw position data', ax=axes)
# smoothen the position data via applying a rolling average
experiment_data.pos = experiment_data.pos.rolling(window=20, center=True).mean()
experiment_data.plot(x='time', y='pos', label='smoothened position', ax=axes, grid=True)
ut.plot_line(slope1[0], intercept1[0]+start_constant, 'sonar position', x_range=[2500, 20000])
plt.show()
