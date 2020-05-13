import pandas as pd

from utils import *

file_path = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'

relevant_cols = 'A:D'
header_row = 1

experiment_data = pd.read_csv(file_path, header=header_row - 1,
                              usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

# smoothen the position data and show the unsmoothed and smoothed data on the same graph
axes = plt.gca()
experiment_data.plot(x='time', y='pos', label='raw position data', ax=axes)
# smoothen the position data via applying a rolling average
experiment_data.pos = experiment_data.pos.rolling(window=20, center=True).mean()

experiment_data.plot(x='time', y='pos', label='smoothened position', ax=axes, grid=True)
plt.show()
