from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler


# "PercentMen", "Hispanic", "White", "Black", "Native", "Asian", "Pacific", "Income", "IncomePerCap", "Poverty",
#      "ChildPoverty", "Professional", "Service", "Office", "Construction", "Production", "Drive", "Carpool", "Transit",
#      "Walk", "OtherTransp", "WorkAtHome", "MeanCommute", "PercentEmployed", "PrivateWork", "PublicWork",
#      "SelfEmployed", "FamilyWork", "Unemployment"

# fix random seed for reproducibility
np.random.seed(7)

def scale(train, test):

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(train)

    train = train.reshape(train.shape[0], train.shape[1])
    train_scaled = scaler.transform(train)

    test = test.reshape(test.shape[0], test.shape[1])
    test_scaled = scaler.transform(test)
    return scaler, train_scaled, test_scaled



def invert_scale(scaler, X, value):
    new_row = [x for x in X] + [value]
    array = np.array(new_row)
    array = array.reshape(1, len(array))
    inverted = scaler.inverse_transform(array)
    return inverted[0, -1]


dataframe = pd.read_csv("census_county_counts.csv")
# split into input (X) and output (Y) variables





dataframe["PercentMen"] = dataframe["Men"] / dataframe["TotalPop"]
dataframe["PercentEmployed"] = dataframe["Employed"] / dataframe["TotalPop"]
dataframe["IncidentsPerCap"] = dataframe["incident_counts"] / dataframe["TotalPop"]

new = dataframe[['PercentMen', 'Poverty', 'PercentEmployed', 'IncidentsPerCap']].copy()
print(new)
scaler = MinMaxScaler(feature_range=(-1,1))
scaler = scaler.fit(new)
scaled_data = scaler.transform(new)
scaled_input = scaled_data[:,0:-1]
scaled_lables = scaled_data[:,-1]
print(scaled_input)
print(scaled_lables)



model = Sequential()
model.add(Dense(12, input_dim=3, activation='linear'))
model.add(Dense(8, activation='linear'))
model.add(Dense(1, activation='linear'))

model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

model.fit(scaled_input, scaled_lables, epochs=50, batch_size=10)

scores = model.evaluate(scaled_input, scaled_lables)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
