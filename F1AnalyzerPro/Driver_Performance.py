import pandas as pd

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

# Merge all important driver data together.
def mergeDriverData (driver):

    # Merges the driver_standings table and the drivers table on the driverId column
    driver_performance = pd.merge(driver_standings, drivers, on='driverId')

    # Removes the column url_x from the table (it is just a source)
    driver_performance.pop('url')

    # Merges the first driver performance with races table
    driver_performance = pd.merge(driver_performance, races, on='raceId')

    # Removes the column url_x from the table (it is just a source)
    driver_performance.pop('url')

    # Gets the driver performance stats based on surname
    # !! returns every driver with the same last name--find future fix
    performance = driver_performance[(driver_performance['surname'] == driver)].copy()

    # Sorts the dataset by the forename
    performance = performance.sort_values('forename')

    # Compares each name to the previous name to see if it is equal. If it is not
    # equal it returns false.
    performance['match'] = performance.forename.eq(performance.forename.shift())

    # Dataframe is created to only hold the data of the names of drivers that have same
    # surname but different forename
    filtered_df = performance[performance['match'] == False]
    print(filtered_df[['surname', 'forename']])
            #return value




