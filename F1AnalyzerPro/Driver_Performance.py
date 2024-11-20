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
    # Filter the performance data for the driver based on the surname
    performance = driver_performance[driver_performance['surname'].str.lower() == driver.lower()]

    # Sort the dataset by forename and reset index
    performance = performance.sort_values('forename').reset_index(drop=True)

    # Find unique forenames for the same surname
    unique_forenames = performance['forename'].unique()

    # If there are multiple drivers with the same surname, ask the user to select a forename
    if len(unique_forenames) > 1:
        print("There are multiple drivers with this surname. Please choose one from the list:")
        print(unique_forenames)

        # Get user input and handle case-insensitive selection
        name_select = input("Select a name: ").strip().capitalize()

        # Ensure the input matches one of the forenames
        while name_select not in unique_forenames:
            print("Invalid selection. Please choose a name from the list.")
            name_select = input("Select a name: ").strip().capitalize()

        # Filter performance data for the selected forename
        performance = performance[performance['forename'] == name_select]

    return performance

# Merge all important driver data together.
def viewMajorDriverData(driver):
    # Call the function to get specific driver data
    performance = getSpecificDriver(driver)

    performance = performance.sort_values('date')
    print(performance.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=performance, x='year', y='position', marker='o')
    plt.title("Driver's Performance Over Time")
    plt.gca().invert_yaxis()  # Lower number is better (1st place is better than 10th)
    plt.xticks(performance['year'].unique())  # Ensure one-year gaps
    plt.xlabel('Year')
    plt.ylabel('Championship Standing Position')
    plt.show()


def driverFinalPointsByYear(driver):
    # Call the function to get specific driver data
    performance = getSpecificDriver(driver)

    # Create dataframe with only the year and points specified
    performance = performance[['year', 'points']].sort_values('year')

    # Get final points by year
    result = performance.groupby('year').tail(1)

    print(result.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=performance, x='year', y='points', marker='o')
    plt.title("Driver's Points By Year")
    plt.gca().invert_yaxis()  # Lower number is better (1st place is better than 10th)
    plt.xticks(performance['year'].unique())  # Ensure one-year gaps
    plt.xlabel('Year')
    plt.ylabel('Championship Standing Position')
    plt.show()


def firstThreeLettersMatch(driver):
    # Setting the driver variable to the first three characters of the name
    driver_prefix = driver[:3].lower()  # Convert to lowercase for case-insensitive matching

    # Filter drivers whose surname contains the first three letters of the input driver name (case-insensitive)
    first_3_check = driver_performance[driver_performance['surname'].str.contains(driver_prefix, case=False, na=False)]

    # Sorts the dataset by forename to make comparison easier
    performance = first_3_check.sort_values('forename')

    # Filter drivers that have the same surname but different forenames
    filtered_df = performance[performance['forename'].ne(performance['forename'].shift())]

    # Print out the drivers with the same surname but different forenames
    print(filtered_df[['surname', 'forename']])  # Showing forename and surname for clarity


def lastThreeLettersMatch(driver):
    # Set the driver variable to the last three characters of the name
    driver_suffix = driver[-3:].lower()  # Convert to lowercase for case-insensitive matching

    # Filter drivers whose surname contains the last three letters of the input driver name (case-insensitive)
    last_3_check = driver_performance[driver_performance['surname'].str.contains(driver_suffix, case=False, na=False)]

    # Sort the dataset by forename for easier comparison
    performance = last_3_check.sort_values('forename')

    # Filter out drivers with the same surname and same forename (no need to use shift() twice)
    filtered_df = performance[performance['forename'].ne(performance['forename'].shift())]

    # Print drivers with the same surname but different forenames
    print(filtered_df[['surname', 'forename']])  # Printing both surname and forename for clarity
