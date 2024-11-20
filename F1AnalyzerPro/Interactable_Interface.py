import tkinter as tk
from tkinter import messagebox
import pandas as pd
from Driver_Performance import *


# Function to search for the points of the given name
def search_points():
    name_input = entry.get().strip()  # Get the name from the text input box
    driver_total_points = viewLifetimeDriverPoints(name_input)
    if name_input:
        # Filter the data for the entered name
        person_data = driver_total_points[driver_performance['name'].str.lower() == name_input.lower()]

        if not person_data.empty:
            # Get the last entry for the person in each year based on the maximum date
            result = person_data.loc[person_data.groupby('year')['date'].idxmax(), ['year', 'points']]

            # Calculate the total points for the person
            total_points = result['points'].sum()

            # Display the result in a message box
            messagebox.showinfo("Total Points", f"{name_input}'s Total Points: {total_points}")
        else:
            # Display a message box if no data found
            messagebox.showwarning("No Data", f"No data found for {name_input}.")
    else:
        # Display a message box if the name input is empty
        messagebox.showwarning("Input Error", "Please enter a name to search.")


# Set up the main window
root = tk.Tk()
root.title("Data Analysis App")

# Create and pack the widgets
label = tk.Label(root, text="Enter Name to Search:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search Points", command=search_points)
search_button.pack(pady=20)

# Run the application
root.mainloop()
