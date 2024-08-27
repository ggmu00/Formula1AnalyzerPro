import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load in the data sets
constructor_results = pd.read_csv('f1_data/constructor_results.csv')
constructors = pd.read_csv('f1_data/constructors.csv')
races = pd.read_csv('f1_data/races.csv')

# Merge all important driver data together.
def viewMajorConstructorData (constructor):

    # Merges the driver_standings table and the drivers table on the driverId column
    constructor_performance = pd.merge(constructor_results, constructors, on='constructorId')

    # Removes columns from the table not vital to driver data
    constructor_performance.pop('url')


    # Merges the first driver performance with races table
    constructor_performance = pd.merge(constructor_performance, races, on='raceId')

    # Removes columns from the table not vital to driver data
    constructor_performance.pop('url')
    constructor_performance.pop('circuitId')
    constructor_performance.pop('raceId')
    constructor_performance=constructor_performance.rename(columns = {'name_y':'raceName'})
    constructor_performance=constructor_performance.rename(columns = {'name_x':'constructorName'})


    # Gets the driver performance stats based on constructor name
    performance = constructor_performance[(constructor_performance['constructorName'] == constructor)].copy()

    print(performance.to_string())
