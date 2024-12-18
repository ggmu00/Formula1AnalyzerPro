import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load in the data sets
driver_standings = pd.read_csv('f1_data/driver_standings.csv')
drivers = pd.read_csv('f1_data/drivers.csv')
races = pd.read_csv('f1_data/races.csv')

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


def getSpecificDriver(driver):
    forename, surname = driver.split(" ", 1)

    # Gets the driver performance stats based on surname
    performance = driver_performance[(driver_performance['forename'] == forename)
                                     & (driver_performance['surname'] == surname)].copy()
    print(performance.to_string())
    return performance


# Merge all important driver data together.
def viewFinalDriverPointsByYear(driver):

    # Call the function to get specific driver data
    # Get specific driver performance data
    performance = getSpecificDriver(driver)

    # Create a dataframe with only relevant columns
    performance = performance[['year', 'points', 'date']]

    # Get the last row for each year based on the maximum date (final points by year)
    result = performance.loc[performance.groupby('year')['date'].idxmax(), ['year', 'points']]
    print(result.to_string())
    return result


def driverFinalPointsByYear(driver):
    # Call the function to get specific driver data
    # Get specific driver performance data
    performance = getSpecificDriver(driver)

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
