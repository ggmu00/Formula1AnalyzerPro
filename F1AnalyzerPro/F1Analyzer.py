from Driver_Performance import *
from Constructor_Performance import *

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

selection_input = input("Type 'C' to browse constuctor data or 'D' to visualize driver data: ").capitalize()

if selection_input == "C":
    name_input = input("Enter a constructor name to see all driver performance data: ").capitalize()
    viewMajorConstructorData(name_input)
elif selection_input == "D":
    name_input = input("Enter a surname to see all driver performance data: ").capitalize()
    #viewMajorDriverData(name_input)
    driverPerformanceByYear(name_input)
