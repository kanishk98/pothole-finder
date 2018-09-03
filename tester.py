import pandas as pd
from keras.models import load_model
import numpy as np
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Feeds standardised data into pre-trained model and generates '
                                             'predictions.')
parser.add_argument('--input', type=str, metavar='File path', help='path to .csv file containing standardised data to '
                                                                   'be tested')
parser.add_argument('--mode', type=int, metavar='N', help='1 to test on accelerometer data, 2 for gyroscope, '
                                                          '3 for both')
args = parser.parse_args()
args_dictionary = vars(args)
model_choice = args_dictionary['mode']

df = pd.read_csv(args_dictionary['input'], error_bad_lines=False)

model_filepath = None
predictions_filepath = None
if model_choice == 1:
    df.drop('GyrX', axis=1, inplace=True)
    df.drop('GyrY', axis=1, inplace=True)
    df.drop('GyrZ', axis=1, inplace=True)
    model_filepath = './model_accelerometer.h5'
    predictions_filepath = './data/test_predictions_accelerometer.csv'
elif model_choice == 2:
    df.drop('AccX', axis=1, inplace=True)
    df.drop('AccY', axis=1, inplace=True)
    df.drop('AccZ', axis=1, inplace=True)
    model_filepath = './model_gyroscope.h5'
    predictions_filepath = './data/test_predictions_gyroscope.csv'
elif model_choice == 3:
    predictions_filepath = './data/test_predictions_accelerometer_and_gyro.csv'
    model_filepath = './model_accelerometer_and_gyro.h5'


df.drop('GeoHash', axis=1, inplace=True)
X_test = df.values
autoencoder = load_model(model_filepath)
predictions = autoencoder.predict(X_test)
mse = np.mean(np.power(X_test - predictions, 2), axis=1)
error_df = pd.DataFrame({'reconstruction_error': mse})
error_array = error_df['reconstruction_error'].values
line_array = []
i = -1
for i in range(len(error_array)):
    line_array.append(i + 1)
plt.hist(error_array)
predictions_file = open(predictions_filepath, 'w')
error_df.to_csv(predictions_file)
i = 0
df = pd.read_csv(args_dictionary['input'], error_bad_lines=False)
geohashes = []
for index in error_df.iterrows():
    if 6.49795 <= error_df.iloc[i][0] <= 13.0633:
        # print(str(error_df.iloc[i][0]) + ' at: ' + str(df.iloc[i][6]) + " line number : " + str(i))
        geohash = str(df.iloc[i][6])
        if geohash not in geohashes:
            geohashes.append(geohash)
    i = i + 1

print(error_df.describe())
print(str(len(geohashes)) + " potholes found.")
print(geohashes)

plt.show()
