import pandas as pd

#load in the data sets
circuits = pd.read_csv('f1_data/circuits.csv')
constructor_results = pd.read_csv('f1_data/constructor_results.csv')
constructors = pd.read_csv('f1_data/constructors.csv')
driver_standings = pd.read_csv('f1_data/driver_standings.csv')
lap_times = pd.read_csv('f1_data/lap_times.csv')
pit_stops = pd.read_csv('f1_data/pit_stops.csv')
qualifying = pd.read_csv('f1_data/qualifying.csv')
races = pd.read_csv('f1_data/races.csv')
results = pd.read_csv('f1_data/results.csv')
sprint_results = pd.read_csv('f1_data/sprint_results.csv')
status = pd.read_csv('f1_data/status.csv')

#first_100_rows_results = pd.read_csv('f1_data/results.csv', nrows=100)
first_100_rows_races = pd.read_csv('f1_data/races.csv', nrows=100)

circuitID_Australia = 1
circuitID_Malaysia = 2

australiaGP_races = races[races['circuitId'] == circuitID_Australia]

#print(first_100_rows_races.to_string())

print(australiaGP_races.to_string())

