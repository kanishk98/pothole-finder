import pandas as pd 
import datetime

df = pd.read_csv('pothole_training_dataset.csv', error_bad_lines=False, verbose=False)
averages_df = pd.read_csv('averages.csv', error_bad_lines=False, verbose=False)
three_seconds_timestamp = []
initial_time_string = df.iloc[0][8][1:]
initial_time = datetime.datetime.strptime(initial_time_string, '%H:%M:%S')
new_time_string = df.iloc[1][8][1:]
new_time = datetime.datetime.strptime(new_time_string, '%H:%M:%S')
diff_time = new_time - initial_time

exit

i = 1
previous_i = 1

z = 1

for row in df.iterrows():
    initial_time_string = df.iloc[z][8][1:]
    sum_accx = 0
    sum_accy = 0
    sum_accz = 0
    sum_gyrx = 0
    sum_gyry = 0
    sum_gyrz = 0
    sum_speed = 0
    diff_time = datetime.datetime.strptime(initial_time_string, '%H:%M:%S') - datetime.datetime.strptime(initial_time_string, '%H:%M:%S')
    while diff_time.seconds < 3: 
        sum_accx = df.iloc[i][0] + sum_accx
        sum_accy = df.iloc[i][1] + sum_accy
        sum_accz = df.iloc[i][2] + sum_accz
        sum_gyrx = df.iloc[i][3] + sum_gyrx
        sum_gyry = df.iloc[i][4] + sum_gyry
        sum_gyrz = df.iloc[i][5] + sum_gyrz
        sum_speed = df.iloc[i][11] + sum_speed
        initial_time = datetime.datetime.strptime(
            initial_time_string, '%H:%M:%S')
        new_time = datetime.datetime.strptime(new_time_string, '%H:%M:%S')
        i = i + 1
        new_time_string = df.iloc[i][8][1:]
        if new_time_string != initial_time_string:
            diff_time = new_time - initial_time
    print(i)
    z = z + i # + 1 needed?
    print(str(sum_accx/(i - previous_i)) + '\t' + str(sum_accy/(i - previous_i)))
    previous_i = i
    # counter will be related to i
    # find averages across these 3 seconds and store them in a list
