import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load in the data sets
circuits = pd.read_csv('f1_data/circuits.csv')
constructor_results = pd.read_csv('f1_data/constructor_results.csv')
constructors = pd.read_csv('f1_data/constructors.csv')
driver_standings = pd.read_csv('f1_data/driver_standings.csv')
drivers = pd.read_csv('f1_data/drivers.csv')
lap_times = pd.read_csv('f1_data/lap_times.csv')
pit_stops = pd.read_csv('f1_data/pit_stops.csv')
qualifying = pd.read_csv('f1_data/qualifying.csv')
races = pd.read_csv('f1_data/races.csv')
results = pd.read_csv('f1_data/results.csv')
seasons = pd.read_csv('f1_data/seasons.csv')
sprint_results = pd.read_csv('f1_data/sprint_results.csv')
status = pd.read_csv('f1_data/status.csv')

#circuitIDs------figure out how to automate this in the future
circuitID_Australia = 1
circuitID_Malaysia = 2
circuitID_Bahrain = 3
circuitID_Spain = 4
circuitID_Turkey = 5
circuitID_Monaco = 6
circuitID_Canada = 7
circuitID_France = 8
circuitID_UK = 9



first_100_rows_results = pd.read_csv('f1_data/constructors.csv', nrows=100)


#australiaGP_races = races[races['circuitId'] == circuitID_Australia]

print(first_100_rows_results.to_string())

# Merge data to get driver standings by year
driver_performance = pd.merge(driver_standings, drivers, on='driverId')
driver_performance = pd.merge(driver_performance, races, on='raceId')




