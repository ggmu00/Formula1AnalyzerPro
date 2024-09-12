# This file will be used to help with search bug fixes.
# For example: User input = Lecrec
# Feedback: "Did you mean Leclerc?"
# Or "Here are some names that might fit the search criteria: "

import pandas as pd
from Driver_Performance import *
from Constructor_Performance import *


def userInput():
    selection_input = input("Type 'C' to browse constuctor data or 'D' to visualize driver data: ").capitalize()

    if selection_input == "C":
        name_input = input("Enter a constructor name to see all driver performance data: ").capitalize()

        #View all major constructor data throughout the years for a specified constructor
        viewMajorConstructorData(name_input)

        # Get the amount of points the constructor had at the end of each year
        constructorFinalPointsByYear(name_input)

    elif selection_input == "D":
        name_input = input("Enter a surname to see all driver performance data: ").capitalize()

        #View all major driver data throughout the years for a specified driver
        #viewMajorDriverData(name_input)

        driverNameCheck(name_input)

        #Get the amount of points the driver had at the end of each year
        driverFinalPointsByYear(name_input)




