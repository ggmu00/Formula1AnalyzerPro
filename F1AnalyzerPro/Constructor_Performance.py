import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load in the data sets
constructor_results = pd.read_csv('f1_data/constructor_results.csv')
constructors = pd.read_csv('f1_data/constructors.csv')
races = pd.read_csv('f1_data/races.csv')


def getSpecificConstructor(constructor):
    # Merges the driver_standings table and the drivers table on the driverId column
    constructor_performance = pd.merge(constructor_results, constructors, on='constructorId')

    # Removes columns from the table not vital to driver data
    constructor_performance.pop('url')
    constructor_performance.pop('constructorResultsId')
    constructor_performance.pop('constructorId')

    # Merges the first driver performance with races table
    constructor_performance = pd.merge(constructor_performance, races, on='raceId')

    # Removes columns from the table not vital to driver data
    constructor_performance.pop('url')
    constructor_performance.pop('circuitId')
    constructor_performance.pop('raceId')
    constructor_performance = constructor_performance.rename(columns={'name_y': 'raceName'})
    constructor_performance = constructor_performance.rename(columns={'name_x': 'constructorName'})

    # Gets the constructor performance stats based on constructor name
    performance = constructor_performance[(constructor_performance['constructorName'] == constructor)].copy()

    return performance


# Merge all important driver data together.
def viewMajorConstructorData(constructor):
    # Call the function to get specific constructor for analysis
    performance = getSpecificConstructor(constructor)

    print(performance.to_string())


def constructorFinalPointsByYear(constructor):
    # Call the function to get specific constructor for analysis
    performance = getSpecificConstructor(constructor)

    # Sort data by date
    performance = performance.sort_values('date')

    #Sum the points by year
    result = performance.groupby('year')['points'].tail(1)

    print(result.to_string())

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=performance, x='year', y='points', marker='o')
    plt.title("Constructor's Points By Year")
    plt.gca().invert_yaxis()  # Lower number is better (1st place is better than 10th)
    plt.xticks(performance['year'].unique())  # Ensure one-year gaps
    plt.xlabel('Year')
    plt.ylabel('Championship Standing Position')
    plt.show()
