import pandas
import datetime
import Geohash
import argparse

parser = argparse.ArgumentParser(description='Standardise logged .csv files to timestamps'
                                             'covering every third of a second.')
parser.add_argument('--input', type=str, metavar='File path', help='path to .csv file containing raw readings'
                                                                   'logged on device')

parser.add_argument('--output', type=str, metavar='File path', help='path to .csv file containing standardised data'
                                                                    'used for training model')

args = parser.parse_args()
args_dictionary = vars(args)

logged_file = args_dictionary['input']
standardised_file = open(args_dictionary['output'], mode='w')
standardised_file.write('AccX,AccY,AccZ,GyrX,GyrY,GyrZ,GeoHash,Speed\n')

df = pandas.read_csv(logged_file, error_bad_lines=False)
timestamp = datetime.datetime.strptime(df.iloc[0][8][1:], '%H:%M:%S')
i = 0
indexes = []
print('Calculating indexes...')

for j in df.iterrows():
    try:
        old_timestamp = timestamp
        while timestamp == old_timestamp:
            old_timestamp = datetime.datetime.strptime(
                df.iloc[i][8][1:], '%H:%M:%S')
            i = i + 1
            timestamp = datetime.datetime.strptime(df.iloc[i][8][1:], '%H:%M:%S')
        indexes.append(i)
    except:
        print('Exception caught, moving on.')
        break

# calculating averages for every third of a second
i = 1
old_j = 0
j_limit = 0
indexes.insert(0, 0)
for index in indexes[1:]:
    old_j = indexes[i - 1]
    for n in range(3):
        sum_accx = 0
        sum_accy = 0
        sum_accz = 0
        sum_gyrx = 0
        sum_gyry = 0
        sum_gyrz = 0
        sum_speed = 0
        sum_latitude = 0
        sum_longitude = 0
        counter = 0
        counter_limit = (index - indexes[i - 1]) // 3
        while (counter < counter_limit):
            # code to add values
            sum_accx = sum_accx + df.iloc[old_j][0]
            sum_accy = sum_accy + df.iloc[old_j][1]
            sum_accz = sum_accz + df.iloc[old_j][2]
            sum_gyrx = sum_gyrx + df.iloc[old_j][3]
            sum_gyry = sum_gyry + df.iloc[old_j][4]
            sum_gyrz = sum_gyrz + df.iloc[old_j][5]
            sum_latitude = sum_latitude + df.iloc[old_j][6]
            sum_longitude = sum_longitude + df.iloc[old_j][7]
            sum_speed = sum_speed + df.iloc[old_j][11]
            sum
            old_j = old_j + 1
            counter = counter + 1
        standardised_file.write(str(sum_accx / counter_limit) + ',' + str(sum_accy / counter_limit) + ',' + str(
            sum_accz / counter_limit) + ',' + str(sum_gyrx / counter_limit) + ',' + str(
            sum_gyry / counter_limit) + ',' + str(sum_gyrz / counter_limit) + ',' + str(
            Geohash.encode(sum_latitude / counter_limit, sum_longitude / counter_limit, precision=8)) + ',' + str(
            sum_speed / counter_limit) + '\n')
    i = i + 1