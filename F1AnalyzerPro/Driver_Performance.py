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
    # Gets the driver performance stats based on surname
    performance = driver_performance[(driver_performance['surname'] == driver)].copy()

    # Sorts the dataset by the forename
    performance = performance.sort_values('forename')

    # Compares each name to the previous name to see if it is equal. If it is not
    # equal it returns false.
    performance['matchName'] = performance.forename.eq(performance.forename.shift())

    # Dataframe is created to only hold the data of the names of drivers that have same
    # surname but different forename
    filtered_df = performance[performance['matchName'] == False]

    # Gets the number of names by getting the amount of rows
    number_of_names = len(filtered_df)

    # Prompting the user for input and storing it in a variable
    if number_of_names > 1:
        # Print drivers with same surname
        print(filtered_df[['forename']])

        name_select = input("There are multiple people with this surname select a name from the above list: ")

        # Displays only the input value drivers
        name_select = name_select.capitalize()
        performance = performance.loc[performance['forename'] == name_select].sort_values('date')

    return performance


# Merge all important driver data together.
def viewLifetimeDriverPoints(driver):
    # Call the function to get specific driver data
    # Get specific driver performance data
    performance = getSpecificDriver(driver)

    # Create a dataframe with only relevant columns
    performance = performance[['year', 'points', 'date']]

    # Get the last row for each year based on the maximum date (final points by year)
    result = performance.loc[performance.groupby('year')['date'].idxmax(), ['year', 'points']]
    total_points = result['points'].sum()
    print(total_points)


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
    plt.ylabel('Championship Standing Position')
    plt.show()
