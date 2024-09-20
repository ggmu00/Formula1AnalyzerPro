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



        # This sets the driver data to the function getFinalPointsByYear;
        # in the future change to pick the data the user wants to see

        check3 = ""

        while check3 == "":
            if name_input not in getSpecificDriver(name_input):
                firstThreeLettersMatch(name_input)
                check = input("Do you see the name you were meaning?(Y/N)").capitalize()
                if check == "Y":
                    name_input = input("Please enter the name exactly as you see in the above list:")
                    check3 = name_input
                    driverFinalPointsByYear(name_input)
                elif check == "N":
                    lastThreeLettersMatch(name_input)
                    check2 = input("Do you see the name you were meaning?(Y/N)")
                    if check2 == "Y":
                        name_input = input("Please enter the name exactly as you see in the above list:")
                        check3 = name_input
                        driverFinalPointsByYear(name_input)
                    elif check2 == "N":
                        check3 = input("Please try again")

        #firstThreeLettersMatch(name_input)
        #getSpecificDriver(lastThreeLettersMatch(name_input))

        #Get the amount of points the driver had at the end of each year
        #driverFinalPointsByYear(name_input)


def driverNameCheck(driver):
    """ driver_df = getSpecificDriver(driver)
    name_input = ""
    print("tahdah")
    first_3_letters_check = driver_df[driver_df["surname"].str.contains(driver[:3])]

    print(first_3_letters_check)

    if driver in getSpecificDriver(driver).values:
        print("work")
        return driver
    elif driver[:3] in first_3_letters_check.values:
        print(first_3_letters_check)
        #getSpecificDriver(driver)
        # getSpecificDriver(driver_first_3)
        # print(name_check)
        #name_input = input("Select your driver from the list above: ")
        #return name_input
    elif driver[-3:] in getSpecificDriver(driver).values[-3:]:
        temp_df = getSpecificDriver(driver)[(getSpecificConstructor(driver)['surname'] == driver[-3:])].copy()
        temp_df = temp_df['matchName'] = temp_df.forename.eq(temp_df.forename.shift())
        filtered_df = temp_df[temp_df['matchName']==True]
        print(filtered_df)
        name_input = input("Select your driver from the list above: ")
        return name_input
    else:
        name_input = input("Please input the name again: ")
        return name_input

        """
