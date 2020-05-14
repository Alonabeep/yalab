import pandas as pd

file_path = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'

relevant_cols = 'A:D'
header_row = 1

experiment_data = pd.read_csv(file_path, header=header_row - 1, usecols=['Time (s)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Temperature (C)': 'temp'})
