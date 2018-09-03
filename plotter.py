import pandas as pd
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Track accelerometer variations over a trip.')
parser.add_argument('--input', type=str, metavar='File path', help='path to .csv file containing raw readings')
args = parser.parse_args()
args_dictionary = vars(args)

filepath = args_dictionary['input']

df = pd.read_csv(filepath, error_bad_lines=False, skipinitialspace=True)
accx = df.AccX.values
accy = df.AccY.values
accz = df.AccZ.values
plt.xlabel('Accelerometer values')
plt.ylabel('Line number')
plt.title('Accelerometer vs Time')
plt.plot(accx, label='AccX')
plt.plot(accy, label='AccY')
plt.plot(accz, label='AccZ')
plt.legend()
plt.show(