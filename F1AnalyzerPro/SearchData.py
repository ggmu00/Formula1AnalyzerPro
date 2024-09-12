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

def driverNameCheck(driver):
    #name_check = getSpecificDriver(driver)
    name_input = ""
    count =0

    while count == 0:
        if driver in getSpecificDriver(driver).values:
            count = count + 1
            return driver
        elif driver[:3] in getSpecificDriver(driver).values[:3]:
            temp_df = getSpecificDriver(driver)[(getSpecificConstructor(driver)['surname'] == driver[:3])].copy()
            temp_df = temp_df['matchName'] = temp_df.forename.eq(temp_df.forename.shift())
            filtered_df = temp_df[temp_df['matchName']==True]
            print(filtered_df)
            name_input = input("Select your driver from the list above: ")
            count = count + 1
            return name_input
        elif driver[-3:] in getSpecificDriver(driver).values[-3:]:
            temp_df = getSpecificDriver(driver)[(getSpecificConstructor(driver)['surname'] == driver[-3:])].copy()
            temp_df = temp_df['matchName'] = temp_df.forename.eq(temp_df.forename.shift())
            filtered_df = temp_df[temp_df['matchName']==True]
            print(filtered_df)
            name_input = input("Select your driver from the list above: ")
            count = count + 1
            return name_input
        else:
            name_input = input("Please input the name again: ")





