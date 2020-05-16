import matplotlib.pyplot as plt
import pandas as pd
import utils as ut
import numpy as np
import seaborn as sns

file_path = '/home/avni1alon/alon/Lab/data/try.csv'

relevant_cols = 'A:D'
header_row = 1
plt.figure('sonar position')

experiment_data = pd.read_csv(file_path, header=header_row - 1,
                              usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})
print(experiment_data.pos)
axes = plt.gca()

## plot real data
# experiment_data.plot(x='time', y='pos', label='raw position data', ax=axes)

# smoothen the position data and show the unsmoothed and smoothed data on the same graph
# smoothen the position data via applying a rolling average
experiment_data.pos = experiment_data.pos.rolling(window=20, center=True).mean()
experiment_data = experiment_data[(experiment_data.pos.notnull())].reset_index()
print(experiment_data)
# normelize the position
experiment_data["pos"] = experiment_data["pos"][0] - experiment_data["pos"]
# fit for position
start_fit_time = 3000
start_fit_index = pd.Index(experiment_data.time).get_loc(start_fit_time)
def test_func(t, a, b):
    return a * t + b
time_for_fit = experiment_data["time"][(experiment_data["time"] > start_fit_time)]
pos_for_fit = experiment_data["pos"][(experiment_data["time"] > start_fit_time)]
slope1, intercept1 = ut.fit_func(test_func, time_for_fit, pos_for_fit)
print(slope1, intercept1)
line_start_pos = experiment_data["pos"][start_fit_index] + intercept1[0]
end_time = 22225
end_index = pd.Index(experiment_data.time).get_loc(end_time)


experiment_data.plot(x='time', y='pos', label='smoothened position', ax=axes, grid=True)
ut.plot_line(slope1[0], line_start_pos, 'sonar position', x_range=[start_fit_time, end_time])

plt.figure('residuals')
line = [test_func(t, slope1[0], intercept1[0]) for t in range(start_fit_time, end_time, 10)]
sns.residplot(experiment_data["time"], experiment_data["pos"])

plt.show()
