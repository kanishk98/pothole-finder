# Pothole Finder Model
Autoencoder-based system to take accelerometer, gyroscope, location, and speed data from an Android device and find out where the phone experienced a pothole.

## File descriptions and explanation

### `standardiser.py`

Standardises the readings obtained from the device to every third of a second. Required so that devices with lower sensor polling rates do not give a differently sized input to the model.

#### Usage

`$ python standardiser.py --input <File path to raw readings file> --output <File path to desired output file>`

If you wish to change the standardising rate from every third of a second to something else, change the following line as indicated:

```
# calculating averages for every third of a second
i = 1
old_j = 0
j_limit = 0
indexes.insert(0, 0)
for index in indexes[1:]:
    old_j = indexes[i - 1]
    for n in range(3): # change 3 to n here for readings to be standardised to every nth of a second`
```

### `pothole_predictor.py`

Trains autoencoder to recognise patterns in the readings of a phone being used over a road with no potholes. 

#### Usage

`$ python pothole_predictor.py --input <File path to standardised training dataset> --mode <1 for considering only accelerometer readings, 2 for considering only gyroscope readings, 3 for both>`

#### Explanation

The model takes in all input features, compresses the same to a single-dimensional layer that represents most essential information in the training dataset. This is then expanded back to the dimensionality of the entire input dataset. 
Using the mean-squared-error as a loss function, thresholds are established after the minimisation of MSE. These thresholds are then used for the `tester.py` script, which is explained below. 

### `tester.py`

Uses model .h5 file generated by `pothole_predictor.py` to output results as per thresholds established according to analysis of the plot output during execution of `pothole_predictor.py`.

#### Usage

`$ python tester.py --input <File path to standardised test dataset> --mode <1 for accelerometer testing, 2 for gyroscope testing, 3 for both>`

#### Explanation

This line deserves most attention:

`if 6.49795 <= error_df.iloc[i][0] <= 13.0633:`

The bounds on the error values isolate the pothole locations to what I term as moderate outliers. The data input into the model can be split into 3 categories according to the reconstruction error values:
1. Least values (0, 6.49795): Not potholes
2. Moderate outliers (6.49795, 13.0633): Potholes
3. Erroneous outliers (> 13.0633): User behaviour-influenced changes in readings (example: picking up a call while logging a trip)

### `model_freezer.py`

Converts the .h5 files generated by Keras to .pb file intended for use in the Android app [Road Quality Audit](https://github.com/padiboi/potholedetector). 

Must be executed before deploying files to the app (TensorFlow for Android cannot read .h5 files)

#### Usage

`$ python model_freezer.py` 

