# Utilities file for storing miscellaneous functions that dont neatly fit into other categories
# (i.e. not models, databases, etc)

import csv
import os

# Set of functions used to read a populate the database from a csv file.
# Checklist for future
# 1. Connect to actual database for population
# 2. Create upload button for frontend that uses these functions
# 3. Remove "if __name__ == "__main__:" and instead incorporate code into Flask

# Reads a CSV file and returns a list of dictionaries where each dictionary represents a row.
def read_csv_file(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    else:
        print(f"The file {file_path} does not exist.")
    return data

# Placeholder function for importing data into the database.
# Currently, this function only prints the data.
def import_data_to_db(data):
    for record in data:
        # Placeholder for DB import logic
        print(f"Importing: {record}")
        # TODO: add the logic to insert the record into the database.

# Process a CSV file by reading it and then importing the data.
def process_csv(file_path):
    # Read the data from the CSV file
    data = read_csv_file(file_path)

    # Import the data to the database (currently just a placeholder)
    import_data_to_db(data)

if __name__ == "__main__":
    # For testing purposes. Remove when integrating into main application
    csv_file_path = '../test.csv'

    # Process the CSV file
    process_csv(csv_file_path)
