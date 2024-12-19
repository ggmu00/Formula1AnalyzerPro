import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load in the data sets
driver_standings = pd.read_csv('f1_data/driver_standings.csv')
drivers = pd.read_csv('f1_data/drivers.csv')
races = pd.read_csv('f1_data/races.csv')
results = pd.read_csv('f1_data/results.csv')

def mergeDriverPointsPerformance():
    # Merges the driver_standings table and the drivers table on the driverId column
    driver_performance = pd.merge(driver_standings, drivers, on='driverId')

    # Removes columns from the table not vital to driver data
    driver_performance.pop('url')
    driver_performance.pop('driverStandingsId')
    driver_performance.pop('driverId')
    driver_performance.pop('dob')
    driver_performance.pop('driverRef')

    # Merges the first driver performance with races table
    driver_performance = pd.merge(driver_performance, races, on='raceId')

    # Removes columns from the table not vital to driver data
    driver_performance.pop('url')
    driver_performance.pop('circuitId')
    driver_performance.pop('raceId')

    driver_performance = driver_performance.rename(columns={'name': 'raceName'})
    results.pop('number')
    return driver_performance

def mergeDriverRacePerformance():

    driver_race_performance=pd.merge(drivers, results, on='driverId')
    driver_race_performance.pop('code')
    driver_race_performance.pop('driverRef')
    driver_race_performance.pop('dob')
    driver_race_performance.pop('url')
    driver_race_performance.pop('driverId')
    driver_race_performance.pop('resultId')
    driver_race_performance.pop('constructorId')
    driver_race_performance.pop('statusId')
    driver_race_performance.pop('number_y')
    driver_race_performance.pop('milliseconds')

    driver_race_performance = driver_race_performance.rename(columns={'number_x': 'driverNumber'})

    driver_race_performance=pd.merge(driver_race_performance, races, on='raceId')
    driver_race_performance.pop('circuitId')
    driver_race_performance.pop('url')
    driver_race_performance.pop('quali_time')
    driver_race_performance.pop('sprint_date')
    driver_race_performance.pop('sprint_time')
    driver_race_performance.pop('quali_date')
    driver_race_performance.pop('fp3_time')
    driver_race_performance.pop('fp3_date')
    driver_race_performance.pop('fp2_time')
    driver_race_performance.pop('fp2_date')
    driver_race_performance.pop('fp1_time')
    driver_race_performance.pop('fp1_date')
    driver_race_performance.pop('time_y')
    driver_race_performance = driver_race_performance.rename(columns={'time_x': 'time'})
    driver_race_performance = driver_race_performance.rename(columns={'name': 'circuitName'})

    return driver_race_performance


def getSpecificDriver(driver,merger):
    forename, surname = driver.split(" ", 1)

    # Gets the driver performance stats based on surname
    performance = merger[(merger['forename'] == forename)
                                     & (merger['surname'] == surname)].copy()
    print(performance.to_string())
    return performance


# Merge all important driver data together.
def viewFinalDriverPointsByYear(driver):

    # Get specific driver performance data
    performance = getSpecificDriver(driver, mergeDriverPointsPerformance())

    # Create a dataframe with only relevant columns
    performance = performance[['year', 'points', 'date']]

    # Get the last row for each year based on the maximum date (final points by year)
    result = performance.loc[performance.groupby('year')['date'].idxmax(), ['year', 'points']]
    print(result.to_string())
    return result

def driverTotalPointsPerRace(driver):
    performance = getSpecificDriver(driver, mergeDriverRacePerformance())

    performance = performance[['circuitName', 'points']]

    result = performance.groupby('circuitName', as_index=False)['points'].sum()

    return result

def driverFinalPointsByYear(driver):
    # Call the function to get specific driver data
    # Get specific driver performance data
    performance = getSpecificDriver(driver, mergeDriverPointsPerformance())

    # Create a dataframe with only relevant columns
    performance = performance[['year', 'points', 'date']]

    # Get the last row for each year based on the maximum date (final points by year)
    result = performance.loc[performance.groupby('year')['date'].idxmax(), ['year', 'points']]

    print(result.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=performance, x='year', y='points', marker='o')
    plt.title("Driver's Points By Year")
    #plt.gca().invert_yaxis()  # Lower number is better (1st place is better than 10th)
    plt.xticks(performance['year'].unique())  # Ensure one-year gaps
    plt.xlabel('Year')
    plt.ylabel('Final Driver Points by Year')
    plt.show()
